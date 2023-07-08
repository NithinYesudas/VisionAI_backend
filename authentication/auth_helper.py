from jose import jwt,JWTError
from models.auth_models import User,UserinDB
from typing import Annotated
from datetime import timedelta,datetime
from fastapi import HTTPException,status,Depends
import os
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer,HTTPBearer,HTTPAuthorizationCredentials
from dotenv import load_dotenv
from database.db_manager import get_one_data


load_dotenv()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")
secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
security_scheme = HTTPBearer()


def get_user(username:str):
    return get_user_from_db(username=username)

def get_hashed_password(password:str):
    return pwd_context.hash(password)

def verify_password(entered_password:str,hashed_password:str):
    return pwd_context.verify(entered_password,hashed_password)
    
def get_user_from_db(username: str) -> dict:
    result = get_one_data({"username": username}, collection="users")
    if result is None:
        return {"username": None, "password": None}
    return {"username": result.get("username"), "password": result.get("password"), "full_name": result.get("full_name"),  "disabled": result.get("disabled")}


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


def verify_token(auth:HTTPAuthorizationCredentials = Depends(security_scheme)):
    try:
        payload = jwt.decode(auth.credentials, secret_key, algorithms=[algorithm])
        if datetime.fromisoformat(payload.get("expires")) < datetime.now():

            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Token expired")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
