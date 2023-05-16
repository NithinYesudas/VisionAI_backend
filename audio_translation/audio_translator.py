import re
from fastapi import File, UploadFile, APIRouter
from fastapi.responses import FileResponse
import io
import os
from audio_translation import translation_handler


router = APIRouter()



@router.post("/translate_audio/")
async def audio(file: UploadFile = File(...)):
    audio_file = await file.read()

    transcript = await translation_handler.get_transcript(audio_file)
    translate = await translation_handler.get_translate(transcript)
    audio_response = await translation_handler.get_translated_audio(translate)

    
    

    return  FileResponse(audio_response,media_type="audio/mp3", filename="translated_output.mp3")
    


