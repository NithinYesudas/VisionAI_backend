from datetime import timedelta
from pydantic import BaseModel
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str = None
    token_type: str = None
    expires: timedelta = None
    
class User(BaseModel):
    username: str
    
    
    full_name: str = None
    disabled: bool = None

class UserinDB(User):
    hashed_password: str