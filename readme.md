# 🎬 Video-to-Text Converter (Whisper + MoviePy)

이 프로젝트는 폴더 내의 `.mp4` 강의 영상을 자동으로  
- 🎧 MP3 오디오로 변환하고  
- 🧠 OpenAI Whisper를 이용해 텍스트로 전사하며  
- 📄 `.txt` 파일로 저장합니다.

---

## 📁 폴더 구조

```bash
vidtosound/
├── videos/        # 입력 영상 (mp4)
├── audios/        # 추출된 mp3 저장
├── texts/         # 추출된 텍스트 저장
├── extract_audio.py
├── requirements.txt
└── README.md
```

---

## 🧪 요구 사항

- Python 3.8 이상
- [ffmpeg](https://ffmpeg.org/)
- pip로 설치 가능한 패키지:

```bash
pip install -r requirements.txt
```

또는 수동 설치 시:

```bash
pip install moviepy
pip install git+https://github.com/openai/whisper.git
```

---

## ⚙️ 실행 방법

```bash
python extract_audio.py
```

- `videos/` 폴더에 있는 모든 `.mp4` 파일이 자동으로 변환됩니다.
- 결과는 `audios/`와 `texts/` 폴더에 저장됩니다.

---

## 🛠 FFmpeg 설치 가이드 (Windows)

`moviepy`와 `whisper`는 내부적으로 `ffmpeg`를 사용하므로, 시스템에 FFmpeg가 설치되어 있어야 합니다.

### ✅ 방법 1: Chocolatey로 설치 (간편)

1. PowerShell을 관리자 권한으로 실행
2. 다음 명령어 입력:

   ```powershell
   choco install ffmpeg
   ```

3. 설치 확인:

   ```powershell
   ffmpeg -version
   ```

---

### ✅ 방법 2: 수동 설치

1. FFmpeg 공식 사이트 접속: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. `Windows builds by gyan.dev` 클릭  
   또는 [직접 다운로드](https://www.gyan.dev/ffmpeg/builds/)

3. `ffmpeg-release-essentials.zip` 압축 해제
4. `bin` 폴더 경로 복사 (예: `C:\ffmpeg\bin`)

5. 시스템 환경 변수 등록:
   - Windows 검색 → `환경 변수 편집`
   - 시스템 변수 → `Path` 편집 → `새로 만들기` → 복사한 경로 붙여넣기

6. 설치 확인:

   ```cmd
   ffmpeg -version
   ```

---

## ✨ 기여 및 문의

> 본 프로젝트는 학습용으로 제작되었습니다.
> 기여, 개선 제안, 버그 제보는 언제든 환영합니다!


---

---

## ⚠️ 저작권 및 사용자 책임 안내

이 프로그램은 개인 학습 및 비상업적 목적의 음성 전사 자동화 도구입니다.  
외부 강의 영상, 방송 콘텐츠 등을 사용할 경우 반드시 아래 사항을 준수하시기 바랍니다:

- 📚 수업 영상이나 상업용 콘텐츠는 대부분 **저작권 보호 대상**입니다.  
- ❌ 원 저작자의 동의 없이 다운로드, 복제, 전사하는 행위는 **저작권법 위반**이 될 수 있습니다.
- ⚖️ 본 프로젝트는 **도구만을 제공**하며, 이를 사용하는 과정에서 발생하는 **모든 법적 책임은 사용자 본인에게 있습니다.**

> **이 프로그램을 사용하는 것은, 사용자가 자신의 사용 행위에 대한 모든 책임을 스스로 부담하는 것에 동의함을 의미합니다.**

---

