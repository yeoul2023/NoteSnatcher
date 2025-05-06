import os
import time
import whisper
import subprocess
from moviepy import VideoFileClip

# 폴더 경로 설정
video_folder = "videos"
audio_folder = "audios"
text_folder = "texts"

# 폴더 생성
for folder in [video_folder, audio_folder, text_folder]:
    os.makedirs(folder, exist_ok=True)

# FFmpeg 경로 확인
def check_ffmpeg():
    try:
        # FFmpeg 버전 확인 시도
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        print("⚠️ FFmpeg가 시스템에 설치되어 있지 않거나 PATH에 등록되지 않았습니다.")
        print("💡 https://ffmpeg.org/download.html 에서 다운로드하고 환경변수에 등록하세요.")
        return False

# FFmpeg 확인
if not check_ffmpeg():
    print("❌ FFmpeg 없이 계속하면 오류가 발생할 수 있습니다.")
    # 선택적으로 여기서 프로그램 종료 가능: exit()

# Whisper 모델 로드 (base, small, medium, large 중 택 1)
print("🔄 Whisper 모델 로딩 중...")
model = whisper.load_model("small")
print("✅ 모델 로딩 완료")

# 모든 MP4 영상 처리
for filename in os.listdir(video_folder):
    if filename.lower().endswith(".mp4"):
        base_name = os.path.splitext(filename)[0]
        video_path = os.path.join(video_folder, filename)
        audio_path = os.path.join(audio_folder, base_name + ".mp3")
        text_path = os.path.join(text_folder, base_name + ".txt")

        print(f"\n🎬 처리 중: {filename} → {base_name}.mp3 → {base_name}.txt")

        try:
            # [1단계] MP4 → MP3 추출
            video = VideoFileClip(video_path)
            video.audio.write_audiofile(audio_path)
            video.close()
            print("✅ 오디오 추출 완료")

            # [2단계] 파일 존재 확인 및 경로 변환
            abs_audio_path = os.path.abspath(audio_path).replace("\\", "/")
            
            if not os.path.exists(abs_audio_path):
                raise FileNotFoundError(f"❌ MP3 파일을 찾을 수 없습니다: {abs_audio_path}")
            
            file_size = os.path.getsize(abs_audio_path) / (1024 * 1024)  # MB 단위
            print(f"✅ MP3 파일 확인: {abs_audio_path} ({file_size:.2f} MB)")
            
            # 파일 시스템 동기화를 위한 대기
            time.sleep(1)

            # [3단계] Whisper로 텍스트 변환 (직접 FFmpeg 경로 지정)
            print("🔄 음성 인식 중... (시간이 걸릴 수 있습니다)")
            
            # 여기서 직접 FFmpeg 경로를 지정하는 방식으로 변경
            # Whisper는 내부적으로 환경변수 FFMPEG_BINARY를 확인함
            os.environ["FFMPEG_BINARY"] = "ffmpeg"  # 시스템 PATH에 있는 ffmpeg 사용
            
            result = model.transcribe(abs_audio_path, language="ko")
            text = result["text"]
            print("✅ 텍스트 변환 완료")

            # [4단계] 텍스트 저장
            with open(text_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"✅ 텍스트 저장 완료: {text_path}")

        except Exception as e:
            print(f"❌ 오류 발생 - {filename}: {str(e)}")
            import traceback
            traceback.print_exc()  # 상세 오류 출력

print("\n🎉 모든 변환 완료!")
