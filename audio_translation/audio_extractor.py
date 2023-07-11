from fastapi import  UploadFile
import os
import librosa
import tempfile

from moviepy.editor import VideoFileClip, AudioFileClip

UPLOADS_DIR = "uploads"
async def extract_audio_from_video(video_file: UploadFile):
    # Create the 'uploads/' directory if it doesn't exist
    if not os.path.exists(UPLOADS_DIR):
        os.makedirs(UPLOADS_DIR)

    # Save the uploaded video file to disk
    file_path = os.path.join(UPLOADS_DIR, "video.mp4")
    with open(file_path, "wb") as f:
        f.write(await video_file.read())

    try:
        # Use moviepy to load the video file
        video = VideoFileClip(file_path)

        # Extract audio from the video
        audio = video.audio

        # Define the output file path for the extracted audio
        audio_file_path = os.path.join(
            UPLOADS_DIR, "audio.mp3")

        # Save the extracted audio to disk
        audio.write_audiofile(audio_file_path)

        # Read the content of the audio file
        with open(audio_file_path, "rb") as f:
            audio_content = f.read()
        del audio
        os.remove(audio_file_path)

        # Return the audio content
        return audio_content

    finally:
        # Delete the uploaded video and audio files from disk
        video.close()
        del video
       

async def replace_audio(audio_path:str):
    # Load the video clip
    video = VideoFileClip("uploads/video.mp4")

    # Load the new audio clip
    audio = AudioFileClip(audio_path)

    # Set the audio of the video to the new audio clip
    video =  video.set_audio(audio)

    # Write the modified video to a new file
    video.write_videofile("uploads/result.mp4", codec="libx264", audio_codec="libmp3lame")
    file_path = os.path.join(UPLOADS_DIR, "result.mp4")
   
    # Close the video and audio clips
    video.close()
    audio.close()
    
    return file_path
