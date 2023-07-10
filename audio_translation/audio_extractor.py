from fastapi import  UploadFile
import os
import librosa

from moviepy.editor import VideoFileClip

UPLOADS_DIR = "uploads"
async def extract_audio_from_video(video_file: UploadFile):
    # Create the 'uploads/' directory if it doesn't exist
    if not os.path.exists(UPLOADS_DIR):
        os.makedirs(UPLOADS_DIR)

    # Save the uploaded video file to disk
    file_path = os.path.join(UPLOADS_DIR, video_file.filename)
    with open(file_path, "wb") as f:
        f.write(await video_file.read())

    try:
        # Use moviepy to load the video file
        video = VideoFileClip(file_path)

        # Extract audio from the video
        audio = video.audio

        # Define the output file path for the extracted audio
        audio_file_path = os.path.join(
            UPLOADS_DIR, f"{video_file.filename.split('.')[0]}.mp3")

        # Save the extracted audio to disk
        audio.write_audiofile(audio_file_path)

        # Read the content of the audio file
        with open(audio_file_path, "rb") as f:
            audio_content = f.read()

        # Return the audio content
        return audio_content

    finally:
        # Delete the uploaded video and audio files from disk
        video.close()
        del video
        del audio
        del file_path


def convert_to_mono(audio_content):


    # Load stereo audio data
    audio_data, sample_rate = librosa.load(audio_content, sr=None, mono=False)

    # Convert to mono by averaging the channels
    mono_audio_data = librosa.to_mono(audio_data)

    # Encode mono audio data as WAV
    mono_audio_content = librosa.util.buf_to_wav(mono_audio_data, sample_rate)

    return mono_audio_content
