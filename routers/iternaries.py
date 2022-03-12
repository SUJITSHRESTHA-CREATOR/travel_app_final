from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import  exc
from schemas import IternaryCreate, IternaryResponse, IternaryUpdate
from models import TrekDestination, User, Itenary
import oauth2, db
from typing import List

router = APIRouter(
    prefix="/travels",
    tags=['Travel Destinations']
)


@router.post("/{id}/itinerary", status_code=status.HTTP_201_CREATED, response_model=IternaryResponse)
def add_itineary(iternary_value: IternaryCreate,  id: int, db: Session = Depends(db.get_db), auth_user : User = Depends(oauth2.get_current_user)):

    trek = db.query(TrekDestination).filter(
        TrekDestination.trek_id == id).first()
    if not trek:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Trek destination does not exist")
    if not trek.user_id == auth_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"Unauthorized")

    new_iter = Itenary(trek_destination_id=id, **iternary_value.dict())

    if iternary_value.day > trek.days:
        trek.days += 1

    try:
        db.add(new_iter)
        db.commit()
        db.refresh(new_iter)
    except exc.IntegrityError:
         raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail=f"day {iternary_value.day} already exists. Update the day or remove the day")
    return new_iter



@router.get("/{id}/itinerary", status_code=status.HTTP_200_OK , response_model=List[IternaryResponse])
def get_itineary_details(id: int, db:Session = Depends(db.get_db)):
    trek = db.query(TrekDestination).filter(
        TrekDestination.trek_id == id).first()
    if not trek:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Trek destination does not exist")
    iter_query = db.query(Itenary).filter(Itenary.trek_destination_id == id).order_by(Itenary.day).all()
    return iter_query


@router.delete("/{id}/itinerary/{day}", status_code=status.HTTP_204_NO_CONTENT)
def delete_itineary(day: int,  id: int, db: Session = Depends(db.get_db), auth_user : User = Depends(oauth2.get_current_user)):

    trek = db.query(TrekDestination).filter(
        TrekDestination.trek_id == id).first()
    if not trek:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Trek destination does not exist")
    if not trek.user_id == auth_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"Unauthorized")

    iter_query = db.query(Itenary).filter(Itenary.trek_destination_id == id,Itenary.day == day)
    if not iter_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"This itinerary does not exist")

    if day == trek.days:
        trek.days -= 1
    iter_query.delete(synchronize_session=False)
    db.commit()
    return f"deleted itineary of day: {day}"


@router.put("/{id}/itinerary/{day}", status_code=status.HTTP_200_OK, response_model=IternaryResponse)
def update_itineary(iternary_value: IternaryUpdate, day: int,  id: int, db: Session = Depends(db.get_db), auth_user : User = Depends(oauth2.get_current_user)):

    trek = db.query(TrekDestination).filter(
        TrekDestination.trek_id == id).first()
    if not trek:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Trek destination does not exist")
    if not trek.user_id == auth_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"Unauthorized")

    iter_query = db.query(Itenary).filter(Itenary.trek_destination_id == id,Itenary.day == day)
    if not iter_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"This itinerary does not exist")
    iter_query.update(iternary_value.dict(), synchronize_session=False)
    db.commit()
    return iter_query.first()