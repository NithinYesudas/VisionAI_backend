
from models.auth_models import Token, User
from typing import Optional
from jose import jwt, JWTError
from datetime import datetime, timedelta

from fastapi import HTTPException, status, Depends
from fastapi.security import  OAuth2PasswordRequestForm
from fastapi import APIRouter
from dotenv import load_dotenv
import os
from database.db_manager import insert_one_data
from authentication import auth_helper


load_dotenv()

router = APIRouter()
 
secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")


@router.post("/auth/register/", response_model=Token)
async def register(form_data: OAuth2PasswordRequestForm = Depends(), full_name: Optional[str] = None):
    if form_data.username is None or form_data.password is None or not form_data.username.__contains__("@"):
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")
    username = auth_helper.get_user(form_data.username).get("username")
    if username == form_data.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    insert_one_data(
        {"username": form_data.username, "password": auth_helper.get_hashed_password(form_data.password), "full_name": full_name,  "disabled": False},collection="users")
    return {"access_token": auth_helper.create_access_token(form_data.username), "refresh_token": auth_helper.create_refresh_token(form_data.username), "token_type": "bearer"}



@router.post("/auth/login/", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username is None or form_data.password is None or not str(form_data.username).__contains__("@"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email")
    user = auth_helper.get_user(form_data.username)
    username = user.get(
        "username")
    if username != form_data.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username")
    
    if not auth_helper.verify_password(form_data.password,  user.get("password")):
        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password")
    if user.get("disabled"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return {"access_token": auth_helper.create_access_token(username, timedelta(minutes=15)), "refresh_token": auth_helper.create_refresh_token(username), "token_type": "bearer"}


@router.post("/auth/refresh/", response_model=Token)
async def refresh_token(token: str):
    data = jwt.decode(token, secret_key, algorithms=[algorithm])
    username = data.get("username")
    if data.get("token_type") != "refresh_token":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    if datetime.fromisoformat(data.get("expires")) < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Token expired")

    return {"access_token": auth_helper.create_access_token(username, timedelta(minutes=15)), "refresh_token": token, "token_type": "bearer"}



@router.get("/user/me/", response_model=User)
async def get_user_me(current_user: User = Depends(auth_helper.get_current_user)):
    return current_user

@router.get("/hello/{message}")
async def hello(message: str):
    return {"hello": message} 