import os
from fastapi import APIRouter
import openai
router = APIRouter()
openai.organization = "org-WCLXqOY552W4pCFBjqvvngoL"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()


@router.get("/hash_tag_generator/{title}")
async def hash_tag_generator(title: str):
    result = openai.Completion.create(
        model="text-davinci-003",
        prompt= f"Create relevant 10 youtube hashtags for the following video title {title}, only give hashtags and exclude any kind of explanations",
        max_tokens=100,
        temperature=0,
    )
    print() 
    return {"message": result["choices"][0]["text"]}
    