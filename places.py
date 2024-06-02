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

