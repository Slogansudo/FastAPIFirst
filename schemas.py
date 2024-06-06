from pydantic import BaseModel
from typing import Optional


class RegisterModel(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: str
    email: str
    password: str

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


class AddressModel(BaseModel):
    name: str


class PlacesModel(BaseModel):
    name: str
    address: AddressModel


class RatePlacesModel(BaseModel):
    rate: int


class TravelCategoryModel(BaseModel):
    author: str
    name: str


class CommentsModel(BaseModel):
    user: str
    text: str


class TravelsModel(BaseModel):
    name: str
    price: Optional[float]
    price_type: str
    description: str
    category: TravelCategoryModel
    palaces: PlacesModel
    comments: CommentsModel
    discounts: Optional[float]


class CheckUserModel(BaseModel):
    username: str
    password: str


class JwtModel(BaseModel):
    authjwt_secret_key: str = '6379e4ca89e82bf7864bed67bb305144bd0ae55e4f78d48672a2b5b7dee82244'
