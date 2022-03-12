from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from db import Base
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.sql.sqltypes import TIMESTAMP


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    full_name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True)
    phone_no = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    routes_written = relationship('TrekDestination', back_populates="created_by") #to get all trekdestinations posted by this user
    # comments_written = relationship('Comment', back_populates='comment_by_user')

class TrekDestination(Base):
    __tablename__ = "trek_destinations"
    trek_id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    days = Column(Integer, nullable=False)
    difficulty = Column(String, nullable=False)
    total_cost = Column(Integer, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    comment_count = Column(Integer, nullable=False, server_default=text('0'))
    vote_count = Column(Integer, nullable=False, server_default=text('0'))
    created_by = relationship("User") #who wrote this trekdestination
    itenaries = relationship("Itenary", back_populates='itenaries', order_by='Itenary.day') #to get all iternaries of the trek destination
    comments = relationship("Comment", back_populates='comments', order_by='Comment.created_at') #to get all comment on the trek_destinations
    votes = relationship('Vote', back_populates='votes')    #to get votes on the trekdestination


class Itenary(Base):
    __tablename__ = 'iternaries'
    trek_destination_id = Column(Integer, ForeignKey("trek_destinations.trek_id", ondelete='CASCADE'), primary_key=True)
    day = Column(Integer, nullable=False, primary_key=True, )
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    day_cost = Column(Integer, nullable=False)
    itenaries = relationship('TrekDestination', back_populates='itenaries')


class Comment(Base):
    __tablename__ ='comments'
    comment_id = Column(Integer, primary_key=True, nullable=False) #isnt there any elegant solution ? 
    comment_on = Column(Integer, ForeignKey("trek_destinations.trek_id", ondelete='CASCADE'))
    comment_by = Column(Integer, ForeignKey("users.id", ondelete= 'CASCADE')) #subject to change to set null
    created_at = Column(                #change it to commented_at. Make new database for this or use alembic
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    comment = Column(String, nullable=False)

    commented_by = relationship('User') 
    comments = relationship('TrekDestination', back_populates='comments')   

class Vote(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    trek_destination_id = Column(Integer, ForeignKey('trek_destinations.trek_id', ondelete='CASCADE'), primary_key=True)
    votes = relationship('TrekDestination', back_populates='votes')
    voted_by = relationship('User')