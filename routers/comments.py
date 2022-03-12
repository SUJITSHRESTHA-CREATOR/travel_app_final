from fastapi import APIRouter, status, HTTPException, Depends
from schemas import CommentCreate, CommentRes, CommentsResponse
from models import TrekDestination, Comment, User
from sqlalchemy.orm import Session
import oauth2
import db
from typing import List

router = APIRouter(
    prefix='/travels',
    tags=['Comment']
)


@router.get("/{id}/comment", status_code=status.HTTP_200_OK, response_model=List[CommentsResponse])
def get_comment_detail(id: int, limit: int = 20, db: Session = Depends(db.get_db)):

    trek = db.query(TrekDestination).filter(
        TrekDestination.trek_id == id).first()
    if not trek:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Trek destination does not exist")
    comment_list = db.query(Comment).order_by(Comment.created_at.desc()).filter(
        Comment.comment_on == id).limit(limit=limit).all()
    return comment_list


@router.post("/{id}/comment", status_code=status.HTTP_201_CREATED, response_model=CommentRes)
def add_comment(commentschema: CommentCreate,  id: int, db: Session = Depends(db.get_db), auth_user: User = Depends(oauth2.get_current_user)):

    trek = db.query(TrekDestination).filter(
        TrekDestination.trek_id == id).first()
    if not trek:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Trek destination does not exist")
    new_comment = Comment(
        comment_on=id, comment_by=auth_user.id, **commentschema.dict())
    db.add(new_comment)
    trek.comment_count += 1
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.put("/{post_id}/comment/{comment_id}", status_code=status.HTTP_201_CREATED, response_model=CommentRes)
def update_comment(commentschema: CommentCreate,  post_id: int, comment_id: int, db: Session = Depends(db.get_db), auth_user: User = Depends(oauth2.get_current_user)):

    trek = db.query(TrekDestination).filter(
        TrekDestination.trek_id == post_id).first()
    if not trek:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Trek destination does not exist")
    comment_query = db.query(Comment).filter(Comment.comment_id == comment_id)
    if not comment_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"comment does not exist")
    if comment_query.first().comment_by == auth_user.id:
        comment_query.update(commentschema.dict(), synchronize_session=False)
        db.commit()
        return comment_query.first()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'not authorized')


@router.delete("/{post_id}/comment/{comment_id}", status_code=status.HTTP_201_CREATED)
def delete_comment(post_id: int, comment_id: int, db: Session = Depends(db.get_db), auth_user: User = Depends(oauth2.get_current_user)):
    trek = db.query(TrekDestination).filter(
        TrekDestination.trek_id == post_id).first()
    if not trek:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Trek destination does not exist")
    comment_query = db.query(Comment).filter(
        Comment.comment_on == post_id, Comment.comment_id == comment_id)
    if not comment_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"comment does not exist")

    if comment_query.first().comment_by == auth_user.id or trek.user_id == auth_user.id:
        comment_query.delete(synchronize_session=False)
        trek.comment_count -= 1
        db.commit()
        return "comment deleted"
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'not authorized')
