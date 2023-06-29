from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, \
    func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from app_db import engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(length=40), nullable=False, unique=True)
    password = Column(String(length=40), nullable=False)
    ads = relationship('Advertisement', back_populates='user')

    def __str__(self):
        return f'User {self.id}: {self.email}'


class Advertisement(Base):
    __tablename__ = 'advertisement'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(length=40), nullable=False)
    description = Column(Text, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User, back_populates='ads')

    def __str__(self):
        return f'Advertisement {self.id}: {self.title} added by User ' \
               f'{self.user_id}'


Base.metadata.create_all(bind=engine)
