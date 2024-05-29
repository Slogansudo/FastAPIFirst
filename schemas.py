from pydantic import BaseModel
from typing import Optional


class RegisterModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True,
        schema_extra = {
            "id": 1,
            "first_name": "John",
            "last_name": "Smith",
            "username": "Smith",
            "email": "example@gmail.com",
            "password": "*****",
            "is_staff": True,
            "is_active": True
        }


class LoginModel(BaseModel):
    username: str
    password: str
