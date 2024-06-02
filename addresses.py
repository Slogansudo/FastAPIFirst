from fastapi import APIRouter
from schemas import AddressModel, PlacesModel, TravelCategoryModel, CommentsModel, TravelsModel
from db.database import Session, ENGINE
from fastapi import HTTPException, status
from db.models import Address, TravelCategory, Travels, Comments, Users, Places

address_router = APIRouter(prefix="/address")
session = Session(bind=ENGINE)


@address_router.get("/")
async def address():
    addresses = session.query(Address).all()
    return addresses


@address_router.post("/")
async def create_address(address: AddressModel):
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


@address_router.get("/{id}")
async def read_address(id: int):
    address = session.query(Address).filter(Address.id == id).first()
    if address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return HTTPException(status_code=status.HTTP_200_OK, detail=address)


@address_router.put("/{id}")
async def update_address(id: int, address: AddressModel):
    exist_address = session.query(Address).filter(Address.id == id).first()
    if exist_address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    exist_address.name = address.name
    session.commit()
    return HTTPException(status_code=status.HTTP_200_OK, detail="address successfully updated")


@address_router.delete("/{id}")
async def delete_address(id: int):
    exist_address = session.query(Address).filter(Address.id == id).first()
    if exist_address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    session.delete(exist_address)
    session.commit()
    return HTTPException(status_code=status.HTTP_200_OK, detail="successfully deleted")
