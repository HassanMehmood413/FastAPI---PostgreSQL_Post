from fastapi import FastAPI , HTTPException , status , Depends
from typing import List
from sqlalchemy.orm import Session
from . import database , models , schema
from .database import engine 
from .routes import posts , users
from .routes import authentication
from .config import  Settings
from .routes import votes

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(authentication.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(votes.router)