import googletrans
from googletrans import Translator,LANGUAGES
import tempfile
from google.oauth2 import service_account
from google.cloud import speech, texttospeech
import os
from dotenv import load_dotenv

load_dotenv()

client_file = os.getenv("GOOLGE_SERVICE_ACCOUNT")
credentials = service_account.Credentials.from_service_account_file(
    client_file)
client_speech = speech.SpeechClient(credentials=credentials)
client_text = texttospeech.TextToSpeechClient(credentials=credentials)


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


async def get_translate(text,dest):
    translator = Translator()

    try:
        
        result = translator.translate(text, dest=dest)
        translated_text = result.text  # Access the translated text 
        return translated_text
    except Exception as e:
        # Handle translation errors
        raise e
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

async def get_supported_languages():
    return LANGUAGES