import os
import whisper
# from moviepy.editor import VideoFileClip
from moviepy import VideoFileClip

from tqdm import tqdm
import json


# Supported media file extensions
AUDIO_EXTENSIONS = ['.mp3', '.wav', '.m4a', '.flac']
VIDEO_EXTENSIONS = ['.mp4', '.mkv', '.avi', '.mov']

def is_media_file(file_path):
    """Check if a file is an audio or video file based on its extension."""
    return any(file_path.lower().endswith(ext) for ext in AUDIO_EXTENSIONS + VIDEO_EXTENSIONS)

def extract_audio_from_video(video_path, audio_path):
    """Extract audio from a video file and save it as a temporary audio file."""
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

def transcribe_media_file(model, file_path, output_folder):
    """Transcribe an audio or video file using the Whisper model."""
    try:
        # If it's a video file, extract audio first
        if any(file_path.lower().endswith(ext) for ext in VIDEO_EXTENSIONS):
            temp_audio_path = os.path.join(output_folder, "temp_audio.wav")
            extract_audio_from_video(file_path, temp_audio_path)
            transcription = model.transcribe(temp_audio_path)
            os.remove(temp_audio_path)  # Clean up temporary audio file
        else:
            transcription = model.transcribe(file_path)

        # Save transcription to a text file
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_file = os.path.join(output_folder, f"{base_name}_transcription.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(transcription["text"])

        # Save transcription to a JSON file
        json_file = os.path.join(output_folder, f"{base_name}_transcription.json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(transcription, f, ensure_ascii=False, indent=4)

        print(f"Transcription saved for: {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_directory(directory, output_folder):
    """Recursively scan a directory for media files and transcribe them."""
    # Load the smallest Whisper model
    model = whisper.load_model("tiny")

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Walk through the directory
    for root, _, files in os.walk(directory):
        for file in tqdm(files, desc="Processing files"):
            file_path = os.path.join(root, file)
            if is_media_file(file_path):
                transcribe_media_file(model, file_path, output_folder)

if __name__ == "__main__":
    # Define the input directory and output folder
    input_directory = input("Enter the directory to scan: ").strip()
    output_directory = os.path.join(input_directory, "transcriptions")

    # Process the directory
    process_directory(input_directory, output_directory)
    print("Transcription process completed.")