
from models.auth_models import Token, TokenData, User, UserinDB
from typing import Optional, Annotated
from jose import jwt, JWTError
from datetime import datetime, timedelta
from pymongo import MongoClient
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter
from dotenv import load_dotenv
import os
load_dotenv()

router = APIRouter()
 

client = MongoClient(
    os.getenv("MONGODB_URL"))
db = client["vision_ai"]
user_collection = db.users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")
secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")


def get_user_from_db(username: str) -> dict:
    result = user_collection.find_one({"username": username})
    if result is None:
        return {"username": None, "password": None}
    return {"username": result.get("username"), "password": result.get("password"), "full_name": result.get("full_name"),  "disabled": result.get("disabled")}


@router.post("/auth/register/", response_model=Token)
async def register(form_data: OAuth2PasswordRequestForm = Depends(), full_name: Optional[str] = None):
    if form_data.username is None or form_data.password is None or not form_data.username.__contains__("@"):
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")
    username = get_user_from_db(form_data.username).get("username")
    if username == form_data.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    user_collection.insert_one(
        {"username": form_data.username, "password": pwd_context.hash(form_data.password), "full_name": full_name,  "disabled": False})
    return {"access_token": create_access_token(form_data.username), "refresh_token": create_refresh_token(form_data.username), "token_type": "bearer"}


def create_access_token(username: str, expires_delta: timedelta | None = None):

    expires = datetime.now()+timedelta(minutes=15)
    print(expires)

    data = {"username": username, "expires": expires.isoformat(),
            "token_type": "access_token"}

    access_token = jwt.encode(data, secret_key, algorithm=algorithm)
    return access_token


def create_refresh_token(username: str):
    expires = datetime.now() + timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRES")))
    data = {"username": username, "expires": expires.isoformat(),
            "token_type": "refresh_token"}

    refresh_token = jwt.encode(data, secret_key, algorithm=algorithm)
    return refresh_token


@router.post("/auth/login/", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username is None or form_data.password is None or not str(username).__contains__("@"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email")
    user = get_user_from_db(form_data.username)
    username = user.get(
        "username")
    if username != form_data.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username")
    
    if not pwd_context.verify(form_data.password,  user.get("password")):
        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password")
    if user.get("disabled"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return {"access_token": create_access_token(username, timedelta(minutes=15)), "refresh_token": create_refresh_token(username), "token_type": "bearer"}


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

    return {"access_token": create_access_token(username, timedelta(minutes=15)), "refresh_token": token, "token_type": "bearer"}


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    data = jwt.decode(token, secret_key, algorithms=[algorithm])
    username = data.get("username")
    if data.get("token_type") != "access_token":
        raise credentials_exception
    if datetime.fromisoformat(data.get("expires")) < datetime.now():

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Token expired"
        )
    user = get_user_from_db(username)
    if user is None:
        raise credentials_exception

    return User(**user)


@router.get("/user/me/", response_model=User)
async def get_user_me(current_user: User = Depends(get_current_user)):
    return current_user
