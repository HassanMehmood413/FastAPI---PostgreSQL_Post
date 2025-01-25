from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

from pydantic.types import conint

# User schema to show user details (used in Post)
class ShowUser(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True 


# Base schema for Post (used for creation)
class PostBase(BaseModel):
    title: str
    content: str
    author: str
    published: bool = True

    class Config:
        orm_mode = True


# Post schema for returning full post data with the owner info
class Post(PostBase):
    id: int
    owner_id: int
    owner: ShowUser  # To include owner info after retrieval from DB

    class Config:
        orm_mode = True


# PostCreate schema for creating a new post
class PostCreate(PostBase):
    class Config:
        orm_mode = True 

        

class PostOut(BaseModel):
    Post: Post
    votes:int
    class Config:
        orm_mode = True 


# User schema
class User(BaseModel):
    username: str
    password: str
    email: EmailStr


# Login schema
class Login(BaseModel):
    email: EmailStr
    password: str


# Token schema for authentication
class Token(BaseModel):
    access_token: str
    token_type: str


# TokenData schema to hold data related to the user (usually after token verification)
class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    # direction either one or zero 
    post_id: int
    direction: int = Field(..., le=1, ge=0)
