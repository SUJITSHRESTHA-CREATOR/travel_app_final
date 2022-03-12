from pydantic import BaseModel
from typing import List
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List


class UserWrittenRoute(BaseModel):
    trek_id: int
    title: str

    class Config:
        orm_mode = True


class UserName(BaseModel):
    full_name: str

    class Config:
        orm_mode = True


class UserNameEmail(UserName):
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(UserNameEmail):
    password: str
    address: Optional[str] = None
    phone_no: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    phone_no: Optional[str] = None
    address: Optional[str] = None

    class Config:
        orm_mode = True


class UserDetailResponse(UserResponse):
    routes_written: List[UserWrittenRoute] = []

    class Config:
        orm_mode = True


class TravelDestinationCreate(BaseModel):
    title: str
    days: int
    difficulty: str
    total_cost: str

    class Config:
        orm_mode = True


class TravelDestinationResponse(BaseModel):
    trek_id: int
    title: str
    days: int
    difficulty: str
    total_cost: str
    created_by: UserName
    comment_count: int
    vote_count: int

    class Config:
        orm_mode = True


class IternaryCreate(BaseModel):
    day: int
    title: str
    description: str
    day_cost: int


class IternaryUpdate(BaseModel):
    title: str
    description: str
    day_cost: int


class IternaryResponse(IternaryCreate):
    class Config:
        orm_mode = True


class UserComment(BaseModel):
    commented_by: UserNameEmail


class CommentCreate(BaseModel):
    comment: str


class CommentRes(BaseModel):
    comment_id: int
    comment: str
    commented_by: UserName

    class Config:
        orm_mode = True


class CommentsResponse(UserComment):
    comment_id: int
    comment: str
    created_at: datetime

    class Config:
        orm_mode = True


class VotedBy(BaseModel):
    voted_by: UserNameEmail

    class Config:
        orm_mode = True


class TravelDestinationDetailResponse(TravelDestinationCreate):
    created_by: UserNameEmail
    created_at: datetime
    itenaries: List[IternaryResponse]
    comments: List[CommentsResponse]
    votes: List[VotedBy]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token : str
    token_type : str

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id : str
    