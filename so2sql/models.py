from stackapi import StackAPI

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Question(Base):
    __tablename__ = 'questions'
    question_id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    creation_date = Column(Integer)
    last_edit_date = Column(Integer)
    last_activity_date = Column(Integer)
    score = Column(Integer)
    answer_count = Column(Integer)
    view_count = Column(Integer)
    comment_count = Column(Integer)
    is_answered = Column(Boolean)
    accepted_answer_id = Column(Integer)
    tags = Column(String)
    owner_user_id = Column(String)

class Answer(Base):
    __tablename__ = 'answers'
    answer_id = Column(Integer, primary_key=True)
    question_id = Column(Integer)
    body = Column(String)
    creation_date = Column(Integer)
    last_edit_date = Column(Integer)
    last_activity_date = Column(Integer)
    score = Column(Integer)
    is_accepted = Column(Boolean)
    owner_user_id = Column(String)

class Comment(Base):
    __tablename__ = 'comments'
    comment_id = Column(Integer, primary_key=True)
    post_id = Column(Integer)
    body = Column(String)
    creation_date = Column(Integer)
    edited = Column(Boolean)
    score = Column(Integer)
    owner_user_id = Column(String)
    reply_to_user_user_id = Column(Integer)