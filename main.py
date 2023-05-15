from fastapi import FastAPI
from auth import router as auth_router
from audio_handler import router as audio_router
from content_generators import router as content_generator_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(audio_router)
app.include_router(content_generator_router)