from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from models import Vote, TrekDestination, User
from schemas import VotedBy
import db, oauth2
from typing import List

router = APIRouter(
    prefix='/travels',
    tags=['Vote']
)

@router.get("/{id}/vote", status_code=status.HTTP_200_OK, response_model=List[VotedBy])
def get_vote_detail(id: int,limit: int = 20, db: Session = Depends(db.get_db)):

    trek = db.query(TrekDestination).filter(TrekDestination.trek_id == id).first()
    if not trek:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Trek destination does not exist")
    vote_list = db.query(Vote).filter(Vote.trek_destination_id == id).limit(limit=limit).all()
    return vote_list

@router.post("/{id}/vote", status_code=status.HTTP_200_OK)
def add_or_remove_vote(id: int, db: Session = Depends(db.get_db), auth_user: User = Depends(oauth2.get_current_user)):

    trek = db.query(TrekDestination).filter(TrekDestination.trek_id == id).first()
    if not trek:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Trek destination does not exist")

    vote_query = db.query(Vote).filter(
        Vote.trek_destination_id == trek.trek_id, Vote.user_id == auth_user.id)

    found_vote = vote_query.first()
    if not found_vote:
        new_vote = Vote(trek_destination_id=id, user_id=auth_user.id)
        db.add(new_vote)
        trek.vote_count += 1
        db.commit()
        return {"message": f"added vote to '{trek.title}' by {auth_user.full_name}"}
    else:
        vote_query.delete(synchronize_session=False)
        trek.vote_count -= 1
        db.commit()
        return {"message": f"removed vote from '{trek.title}' given by {auth_user.full_name}"}

