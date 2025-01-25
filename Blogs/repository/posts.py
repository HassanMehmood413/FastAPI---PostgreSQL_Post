from fastapi import APIRouter , HTTPException , status , Depends
from sqlalchemy.orm import Session
from typing import Optional
from .. import models,schema,database , oauth2
from sqlalchemy import func

get_db = database.get_db


get_current_user = oauth2.get_current_user

def get_all_posts(db: Session = Depends(get_db),limit:int = 10,skip:int = 0,search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post,func.count(models.Votes.post_id).label('votes')).join(models.Votes,models.Votes.post_id
                == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results



def create_new_post(post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print("Current User:", current_user)  # This will print the user object if the token is valid
    new_post = models.Post(owner_id=current_user.id , **post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post



def get_spec_post(id: int , db: Session = Depends(get_db)):

    post = db.query(models.Post,func.count(models.Votes.post_id).label('votes')).join(models.Votes,models.Votes.post_id
                 == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post



def delete_any_post(id: int, db: Session = Depends(get_db), current_user :int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # user can delete their own posts, not others
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this post")

    db.delete(post)
    db.commit() 

    return {"message": "Post deleted successfully"}


def update_any_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    post_to_update = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post_to_update:
        raise HTTPException(status_code=404, detail="Post not found")
    
    
    if post_to_update.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to Update this post")


    for key, value in post.dict().items():
        print(key,value)
        setattr(post_to_update, key, value)
    
    db.commit()
    return {"message": "Post updated successfully"}





# def update_any_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db), current_user: schema.TokenData = Depends(oauth2.get_current_user)):
#     post_to_update = db.query(models.Post).filter(models.Post.id == id).first()

#     if not post_to_update:
#         raise HTTPException(status_code=404, detail="Post not found")

#     # Ensure the user can only update their own posts
#     if post_to_update.owner_id != current_user.id:
#         raise HTTPException(status_code=403, detail="You are not allowed to update this post")

#     # Update the post fields
#     for key, value in post.dict().items():
#         setattr(post_to_update, key, value)

#     db.commit()
#     return {"message": "Post updated successfully"}

