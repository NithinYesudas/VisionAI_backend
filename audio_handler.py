import re
from fastapi import File, UploadFile, APIRouter
from fastapi.responses import FileResponse
import io
import os
from google.oauth2 import service_account
from google.cloud import speech, texttospeech
import googletrans
from googletrans import Translator
import tempfile

router = APIRouter()

client_file = os.getenv("GOOLGE_SERVICE_ACCOUNT")
credentials = service_account.Credentials.from_service_account_file(
    client_file)
client_speech = speech.SpeechClient(credentials=credentials)
client_text = texttospeech.TextToSpeechClient(credentials=credentials)


@router.post("/audio/")
async def audio(file: UploadFile = File(...)):
    audio_file = await file.read()

    transcript = await get_transcript(audio_file)
    translate = await get_translate(transcript)
    audio_response = await get_translated_audio(translate)

    
    

    return  FileResponse(audio_response,media_type="audio/mp3", filename="translated_output.mp3")
    


async def get_transcript(audio_file):
    audio = speech.RecognitionAudio(content=audio_file)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
    )

    response = client_speech.recognize(config=config, audio=audio)
    print(response)

    if response.results:
        return response.results[0].alternatives[0].transcript
    else:
        return ""




async def get_translate(text):
    translator = Translator()

    try:
        result = translator.translate(text, dest='ml')
        translated_text = result.text  # Access the translated text
        return translated_text
    except Exception as e:
        # Handle translation errors
        print(f"Translation error: {str(e)}")
        return ""


async def get_translated_audio(text):
    input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code='es',
        name='ml-IN-Standard-B',
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client_text.synthesize_speech(
        request={"input": input, "voice": voice, "audio_config": audio_config}
    )

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        temp_file.write(response.audio_content)
        temp_file_path = temp_file.name

    return temp_file_path
