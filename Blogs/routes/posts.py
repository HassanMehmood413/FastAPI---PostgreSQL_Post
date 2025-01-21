from typing import List , Optional
from fastapi import APIRouter , HTTPException , status , Depends
from sqlalchemy.orm import Session
from .. import models,schema,database , oauth2
from ..repository import posts




router = APIRouter(
    tags=['Post'],
    prefix="/posts"
)


get_db = database.get_db

@router.get("/",status_code=status.HTTP_200_OK,response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db), current_user :int = Depends(oauth2.get_current_user),limit:int =10 ,skip:int = 0,search: Optional[str] = ""):
    return posts.get_all_posts(db,limit,skip,search)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    return posts.create_new_post(post, db, current_user) 
# Wasted my whole day cuz i did not pass the current_user HAHAHAHAHAHAHA Just did the stupiest thing ever :D


@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schema.Post)
def get_post(id: int , db: Session = Depends(get_db), current_user :int = Depends(oauth2.get_current_user)):
    return posts.get_spec_post(id,db)



@router.delete('/{id}',status_code=status.HTTP_200_OK)
def delete_post(id: int, db: Session = Depends(get_db), current_user :int = Depends(oauth2.get_current_user)):
    return posts.delete_any_post(id,db,current_user)



@router.put('/{id}', status_code=status.HTTP_200_OK)
def update_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db), current_user :int = Depends(oauth2.get_current_user)):
    return posts.update_any_post(id,post,db,current_user)

