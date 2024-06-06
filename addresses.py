from fastapi import APIRouter
from schemas import AddressModel, PlacesModel, TravelCategoryModel, CommentsModel, TravelsModel, CheckUserModel
from db.database import Session, ENGINE
from fastapi import HTTPException, status, Depends
from db.models import Address, TravelCategory, Travels, Comments, Users, Places
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from datetime import datetime

address_router = APIRouter(prefix="/address")
session = Session(bind=ENGINE)


@address_router.get("/")
async def address(Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    addresses = session.query(Address).all()
    return addresses


@address_router.post("/")
async def create_address(address: AddressModel, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    if exist_user.is_staff:
        addresses = session.query(Address).filter(Address.name == address.name).first()
        if addresses is None:
            new_address = Address(
                name=address.name
            )
            session.add(new_address)
            session.commit()
            session.refresh(new_address)
            return HTTPException(status_code=status.HTTP_201_CREATED, detail=new_address)
        else:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Address already exists")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="It is not possible to view user data for you")


@address_router.get("/top")
async def top_looking_address(Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    addresses = session.query(Address).order_by(-Address.loking_count).limit(3).all()
    return HTTPException(status_code=status.HTTP_200_OK, detail=addresses)


@address_router.get("/new_address")
async def new_address(Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    addresses = session.query(Address).filter(Address.created_date >= datetime.now().date()).all()
    return HTTPException(status_code=status.HTTP_200_OK, detail=addresses)


@address_router.get("/{id}")
async def read_address(id: int, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    address = session.query(Address).filter(Address.id == id).first()
    if address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    address.loking_count += 1
    session.commit()
    session.refresh(address)
    return HTTPException(status_code=status.HTTP_200_OK, detail=address)


@address_router.put("/{id}")
async def update_address(id: int, address: AddressModel, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    if exist_user.is_staff:
        exist_address = session.query(Address).filter(Address.id == id).first()
        if exist_address is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        exist_address.name = address.name
        session.commit()
        return HTTPException(status_code=status.HTTP_200_OK, detail="address successfully updated")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="It is not possible to view user data for you")


@address_router.delete("/{id}")
async def delete_address(id: int, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    if exist_user.is_staff:
        exist_address = session.query(Address).filter(Address.id == id).first()
        if exist_address is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        session.delete(exist_address)
        session.commit()
        return HTTPException(status_code=status.HTTP_200_OK, detail="successfully deleted")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="It is not possible to view user data for you")




