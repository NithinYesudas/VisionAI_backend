import os
from openai_handler import openai_prompt_runner
from fastapi import APIRouter

router = APIRouter()




@router.get("/hash_tag_generator/{title}")
async def hash_tag_generator(title: str):
    result = openai_prompt_runner(f"Generate 10 relevant hash tags for the following video title {title}, please avoid any kind of explanations other that the hash tag of the video")
     
    return {"hash_tags": result}
@router.get("/description_generator/{title}")
async def description_generator(title: str):
    result = openai_prompt_runner(f"Generate a relevant description for the following video title {title}, please avoid any kind of explanations other that the description of the video")
    return {"description": result}