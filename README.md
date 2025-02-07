# Transcription-Audio-Video

# Media Transcription Script

This Python script transcribes audio and video files in a given directory. It uses the Whisper model to transcribe audio and video files into text. For video files, it extracts the audio before transcription. The transcription is saved in both text and JSON formats.

## Requirements

Before using this script, you need to install the required dependencies.

### Download ffmpeg First => https://ffmpeg.org/download.html

```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Dependencies:
- `whisper`: For transcribing audio and video files.
- `moviepy`: For extracting audio from video files.
- `tqdm`: For showing progress bars during processing.
- `json`: For saving transcription in JSON format (built-in Python library).
- `os`: For interacting with the file system (built-in Python library).


