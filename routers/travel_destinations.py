from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas import TravelDestinationCreate, TravelDestinationDetailResponse, TravelDestinationResponse
from models import TrekDestination, User
import oauth2, db
from typing import Optional
router = APIRouter(
    prefix="/travels",
    tags=['Travel Destinations']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=TravelDestinationResponse)
def create_trek_destination(trek: TravelDestinationCreate, db: Session = Depends(db.get_db),
                            auth_user: User = Depends(oauth2.get_current_user)):
    new_trek = TrekDestination(user_id=auth_user.id, **trek.dict())
    db.add(new_trek)
    db.commit()
    db.refresh(new_trek)
    return new_trek


@router.get('/', response_model=List[TravelDestinationResponse], status_code=status.HTTP_200_OK)
def get_all_travel_destinations(limit: int = 10, skip: int = 0, search: Optional[str] = "", db: Session = Depends(db.get_db)):

    treks = db.query(TrekDestination).order_by(TrekDestination.trek_id).filter(
        TrekDestination.title.contains(search.lower())).limit(limit=limit).offset(skip).all()
    if treks:
        return treks


@router.get('/{id}', response_model=TravelDestinationDetailResponse)
def get_trek_destination_by_id(id: int, db: Session = Depends(db.get_db)):
    trek = db.query(TrekDestination).filter(
        TrekDestination.trek_id == id).first()

    if trek:
        return trek
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'trek route with id = {id} not found')


@router.put('/{id}', response_model=TravelDestinationResponse, status_code=status.HTTP_200_OK)
def update_trek_destination(id: int,
                            trek: TravelDestinationCreate,
                            auth_user: User = Depends(oauth2.get_current_user),
                            db: Session = Depends(db.get_db)):

    trek_query = db.query(TrekDestination).filter(
        TrekDestination.trek_id == id)

    if trek_query.first():
        if trek_query.first().user_id == auth_user.id:
            trek_query.update(trek.dict(), synchronize_session=False)
            db.commit()
            return trek_query.first()
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f'not authorized')

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'trek with id={id} not found')


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_trek_destination(id: int, db: Session = Depends(db.get_db), auth_user: User = Depends(oauth2.get_current_user)):

    trek = db.query(TrekDestination).filter(TrekDestination.trek_id == id)
    if trek.first():
        if trek.first().user_id == auth_user.id:
            trek.delete(synchronize_session=False)
            db.commit()
            return "deleted"
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f'not authorized')

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'post with id = {id} not found')
