from fastapi import APIRouter , HTTPException , status , Depends
from .. import database,schema,models,oauth2
from sqlalchemy.orm import Session






def create_new_vote(vote:schema.Vote,db: Session = Depends(database.get_db),current_user :int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id,models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.direction == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already voted for this post")
        else:
            new_vote = models.Votes(user_id=current_user.id,post_id=vote.post_id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
            return {"message": "Vote created successfully"}
    elif (vote.direction == 0):
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have not voted for this post")
        else:
            db.delete(found_vote)
            db.commit()
            return {"message": "Vote deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid vote direction")