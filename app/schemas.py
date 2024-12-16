from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content:str 
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime

    
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    

    # class Config:
    #     orm_mode = True

class UserCreate(BaseModel):
    email:EmailStr
    password:str



class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str] = None


class Vote(BaseModel):
    post_id:int 
    dir: int

class PostBase2(BaseModel):
    title: str
    content: str
    created_at: str
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True  # Tells Pydantic to treat SQLAlchemy models as dict-like

class PostWithVotes(PostBase):
    votes: int  # Include the votes field