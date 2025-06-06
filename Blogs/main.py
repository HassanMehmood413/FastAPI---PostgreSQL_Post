from fastapi import FastAPI
from . import models 
from .database import engine 
from .routes import posts , users
from .routes import authentication
from fastapi.middleware.cors import CORSMiddleware
from .routes import votes

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(authentication.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(votes.router)