from fastapi import FastAPI
from authentication.auth import router as auth_router
from audio_translation.audio_translator import router as audio_router
from content_generator.content_generators import router as content_generator_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(audio_router)
app.include_router(content_generator_router)