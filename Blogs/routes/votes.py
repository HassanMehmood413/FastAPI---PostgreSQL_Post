from fastapi import APIRouter , HTTPException , status , Depends
from .. import database,schema,models,oauth2
from sqlalchemy.orm import Session
from ..repository import votes


router = APIRouter(
    tags=['Vote'],
    prefix="/votes"
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_vote(vote:schema.Vote,db: Session = Depends(database.get_db),current_user :int = Depends(oauth2.get_current_user)):
    return votes.create_new_vote(vote,db,current_user)