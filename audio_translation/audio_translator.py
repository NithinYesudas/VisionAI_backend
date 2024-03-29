import re
from fastapi import File, UploadFile, APIRouter
from fastapi.responses import FileResponse
import io
import os
from audio_translation import translation_handler
from audio_translation import audio_extractor


router = APIRouter()


@router.post("/translate_audio/{dest}")
async def audio(dest: str,file: UploadFile = File(...)):
    audio_file = await audio_extractor.extract_audio_from_video(file)
    
    transcript = await translation_handler.get_transcript(audio_file)
    translate = await translation_handler.get_translate(transcript,dest)
    audio_response = await translation_handler.get_translated_audio(translate)
    video_file = await audio_extractor.replace_audio(audio_response)
    
    return FileResponse(video_file, media_type="video/mp4", filename="translated_output.mp4")


@router.get("/languages/")
async def languages():
    return await translation_handler.get_supported_languages()
