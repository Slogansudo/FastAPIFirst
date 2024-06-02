from fastapi import APIRouter
from schemas import AddressModel, PlacesModel, TravelCategoryModel, CommentsModel, TravelsModel
from db.database import Session, ENGINE
from fastapi import HTTPException, status
from db.models import Address, TravelCategory, Travels, Comments, Users, Places

places_router = APIRouter(prefix="/places")
session = Session(bind=ENGINE)


@places_router.get("/")
async def get_places():
    places = session.query(Places).all()
    return places


@places_router.post("/")
async def create_place(place: PlacesModel):
    existing_address = session.query(Address).filter(Address.name == place.address.name).first()
    if existing_address is None:
        new_address = Address(name=place.address.name)
        session.add(new_address)
        session.commit()
        session.refresh(new_address)
        address_id = new_address.id
    else:
        address_id = existing_address.id

    existing_place = session.query(Places).filter(Places.name == place.name).first()
    if existing_place is None:
        new_place = Places(
            name=place.name,
            address_id=address_id
        )
        session.add(new_place)
        session.commit()
        session.refresh(new_place)
        return {"message": "Place created successfully", "place": new_place}
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Place already exists")


@places_router.get("/{id}")
async def get_place(id: int):
    place = session.query(Places).filter(Places.id == id).first()
    if place is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return HTTPException(status_code=status.HTTP_200_OK, detail=place)


@places_router.put("/{id}")
async def update_place(id: int, place: PlacesModel):
    exist_place = session.query(Places).filter(Places.id == id).first()
    if exist_place is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    exist_places = session.query(Places).filter(Places.name == place.name).first()
    if exist_places:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Place already exists")
    exist_address = session.query(Address).filter(Address.name == place.address.name).first()
    if exist_address is None:
        new_address = Address(name=place.address.name)
        session.add(new_address)
        session.commit()
        exist_place.address_id = new_address.id
        exist_place.name = place.name
        session.commit()
        return HTTPException(status_code=status.HTTP_200_OK, detail="succesfully updated")
    else:
        exist_place.address_id = exist_address.id
        exist_place.name = place.name
        session.commit()
        return HTTPException(status_code=status.HTTP_200_OK, detail="succesfully updated")


@places_router.delete("/{id}")
async def delete_place(id: int):
    exist_place = session.query(Places).filter(Places.id ==id).first()
    if exist_place is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    session.delete(exist_place)
    session.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
