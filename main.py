from fastapi import FastAPI
from auth import router as auth_router
from audio_handler import router as audio_router
from hash_tag_generator import router as hash_tag_generator_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(audio_router)
app.include_router(hash_tag_generator_router)