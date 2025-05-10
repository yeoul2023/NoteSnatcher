import os
import time
import whisper
import subprocess
import torch
import ffmpeg
import json

# ✅ [함수] MP4 → MP3 오디오 추출 함수 (ffmpeg-python 사용)
def extract_audio_ffmpeg(input_path, output_path):
    # libmp3lame 코덱으로 고음질 추출, qscale=2는 고정 비트레이트 수준
    ffmpeg.input(input_path).output(output_path, acodec="libmp3lame", qscale=2).run()

# ✅ [함수] FFmpeg 설치 여부 확인 함수
def check_ffmpeg():
    try:
        # ffmpeg 버전 명령 실행 성공 시 → 설치된 것
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        print("⚠️ FFmpeg가 설치되어 있지 않거나 PATH에 없습니다.")
        return False

# ✅ [함수] Whisper 결과를 txt 또는 json 파일로 저장하는 함수
def save_transcript(result, text_path, output_format):
    lang = result.get("language", "unknown")         # 자동 감지된 언어
    segments = result.get("segments", [])            # 문장 단위 segment 리스트

    # ✅ JSON 저장
    if output_format in ("json", "both"):
        json_data = {
            "language": lang,
            "segments": [
                {
                    "start": seg["start"],
                    "end": seg["end"],
                    "text": seg["text"].strip()
                } for seg in segments
            ]
        }
        json_path = text_path.replace(".txt", ".json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON 저장 완료: {json_path}")

    # ✅ TXT 저장
    if output_format in ("txt", "both"):
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(f"# 감지된 언어: {lang}\n\n")
            for seg in segments:
                f.write(f"[{seg['start']:.2f} ~ {seg['end']:.2f}] {seg['text'].strip()}\n")
        print(f"✅ TXT 저장 완료: {text_path}")

# ✅ 디렉토리 자동 생성 (없으면 생성)
video_folder = "videos"
audio_folder = "audios"
text_folder = "texts"
for folder in [video_folder, audio_folder, text_folder]:
    os.makedirs(folder, exist_ok=True)

# ✅ FFmpeg 설치 확인
if not check_ffmpeg():
    exit()  # 설치 안 된 경우 프로그램 종료

# ✅ Whisper 모델 로딩 및 환경 설정
print("🔄 Whisper 모델 로딩 중...")
use_cuda = torch.cuda.is_available()            # CUDA(GPU) 사용 가능한지 확인
device = "cuda" if use_cuda else "cpu"          # CUDA 있으면 'cuda', 없으면 'cpu'
fp16 = use_cuda                                 # GPU가 있으면 float16으로 연산 최적화
model = whisper.load_model("base").to(device)   # Whisper 모델 로딩 및 장치 지정
print(f"✅ Whisper 모델 로딩 완료: device={device}, fp16={fp16}")

# ✅ 사용자로부터 출력 형식(txt/json/both) 입력 받기
valid_choices = ["txt", "json", "both"]
output_format = input("출력 형식을 선택하세요 (txt / json / both): ").strip().lower()
while output_format not in valid_choices:
    print("❌ 잘못된 선택입니다. 다시 입력하세요.")
    output_format = input("출력 형식을 선택하세요 (txt / json / both): ").strip().lower()

# ✅ 영상 파일 반복 처리
for filename in os.listdir(video_folder):
    if filename.lower().endswith(".mp4"):  # MP4 파일만 처리
        base_name = os.path.splitext(filename)[0]
        video_path = os.path.join(video_folder, filename)
        audio_path = os.path.join(audio_folder, base_name + ".mp3")
        text_path = os.path.join(text_folder, base_name + ".txt")

        print(f"\n🎬 처리 중: {filename}")

        try:
            # ✅ [1단계] 오디오 추출 (이미 있으면 생략)
            if not os.path.exists(audio_path):
                extract_audio_ffmpeg(video_path, audio_path)
                print("✅ 오디오 추출 완료 (ffmpeg)")
            else:
                print("🟡 기존 MP3 존재 → 추출 생략")

            # ✅ [2단계] Whisper 음성 인식
            abs_audio_path = os.path.abspath(audio_path).replace("\\", "/")  # Windows 경로 호환
            if not os.path.exists(abs_audio_path):
                raise FileNotFoundError(f"❌ MP3 파일을 찾을 수 없습니다: {abs_audio_path}")

            file_size = os.path.getsize(abs_audio_path) / (1024 * 1024)
            print(f"✅ MP3 파일 확인: {abs_audio_path} ({file_size:.2f} MB)")

            time.sleep(1)  # 파일 시스템 안정화 대기 (특히 Windows)

            os.environ["FFMPEG_BINARY"] = "ffmpeg"  # 일부 내부 처리용 (사실상 whisper에는 영향 없음)

            print("🔄 음성 인식 중...")
            result = model.transcribe(abs_audio_path, language=None, fp16=fp16)  # 자동 언어 감지 + float16 최적화

            # ✅ [3단계] 결과 저장 (txt/json/both)
            save_transcript(result, text_path, output_format)

        except Exception as e:
            print(f"❌ 오류 발생 - {filename}: {str(e)}")
            import traceback
            traceback.print_exc()

print("\n🎉 모든 변환 완료!")