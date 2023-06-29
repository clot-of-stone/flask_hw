from typing import Optional
from pydantic import BaseModel, validator


class AdvCreating(BaseModel):
    title: str
    description: str
    user_id: int


class AdvEditing(BaseModel):
    title: Optional[str]
    description: Optional[str]


class UserCreating(BaseModel):
    email: str
    password: str

    @validator('password')
    def validate_password(cls, value: str):
        if len(value) > 7:
            if value.isnumeric() or value.isalpha():
                raise ValueError(
                    'password must not contain only letters or digits')
        else:
            raise ValueError('password must be 8 symbols or more')
        return value


class UserEditing(BaseModel):
    email: Optional[str]
    password: Optional[str]

    @validator('password')
    def validate_password(cls, value: str):
        if len(value) > 7:
            if value.isnumeric() or value.isalpha():
                raise ValueError(
                    'password must not contain only letters or digits')
        else:
            raise ValueError('password must be 8 symbols or more')
        return value
