import os
from moviepy import VideoFileClip

# 폴더 경로 설정
video_folder = "videos"
audio_folder = "audios"

# 오디오 저장 폴더 없으면 생성
if not os.path.exists(audio_folder):
    os.makedirs(audio_folder)

# videos 폴더 내 모든 .mp4 파일 처리
for filename in os.listdir(video_folder):
    if filename.lower().endswith(".mp4"):
        video_path = os.path.join(video_folder, filename)
        
        # 파일 이름 (확장자 제거)
        base_name = os.path.splitext(filename)[0]
        audio_path = os.path.join(audio_folder, base_name + ".mp3")

        print(f"🎬 변환 중: {filename} → {base_name}.mp3")

        try:
            video = VideoFileClip(video_path)
            audio = video.audio
            audio.write_audiofile(audio_path)
            video.close()
        except Exception as e:
            print(f"❌ 오류 발생 - {filename}: {e}")

print("✅ 모든 변환 완료!")
