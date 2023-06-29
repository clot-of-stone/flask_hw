from hashlib import md5
from typing import Type
from pydantic import ValidationError
from app_db import Session
from models import Advertisement, User
from errors import HttpError
from rules import AdvCreating, AdvEditing, UserCreating, UserEditing


def validate(data: dict, validations: Type[AdvCreating] | Type[
    AdvEditing] | Type[UserCreating] | Type[UserEditing]):
    try:
        example = validations(**data)
        return example.dict(exclude_none=True)
    except ValidationError as error:
        raise HttpError(400, error.errors())


def get_adv(adv_id: int, session: Session):
    adv = session.get(Advertisement, adv_id)
    if adv is None:
        raise HttpError(404, 'Advertisement\'s not found')
    return adv


def get_user(user_id: int, session: Session):
    user = session.get(User, user_id)
    if user is None:
        raise HttpError(404, 'User\'s not found')
    return user


def hash_password(password: str):
    return md5(password.encode()).hexdigest()
