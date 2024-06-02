from fastapi import APIRouter
from schemas import AddressModel, PlacesModel, TravelCategoryModel, CommentsModel, TravelsModel
from db.database import Session, ENGINE
from fastapi import HTTPException, status
from db.models import Address, TravelCategory, Travels, Comments, Users, Places


session = Session(bind=ENGINE)
travel_router = APIRouter(prefix='/travel')


@travel_router.get("/")
async def travels_get():
    travels = session.query(Travels).all()
    return travels


@travel_router.post("/")
async def create_travels(travel: TravelsModel):
    exist_travel = session.query(Travels).filter(Travels.name == travel.name).first()
    if exist_travel:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Travel is alredy exist")
    else:
        exist_travel_category = session.query(TravelCategory).filter(TravelCategory.name == travel.category.name).first()
        if exist_travel_category:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="TravelCategory is alredy exist")
        else:
            exist_places = session.query(Places).filter(Places.name == travel.palaces.name).first()
            if exist_places:
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Places is already exist")
            else:
                exist_address = session.query(Address).filter(Address.name == travel.palaces.address.name).first()
                if exist_address:
                    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Address is alredy exist")
                else:
                    exist_author = session.query(Users).filter(Users.username == travel.category.author).first()
                    if exist_author:
                        new_category = TravelCategory(
                            author_id=exist_author.id,
                            name=travel.category.name
                        )
                        session.add(new_category)
                        session.commit()
                        session.refresh(new_category)
                        new_address = Address(
                            name=travel.palaces.address.name
                        )
                        session.add(new_address)
                        session.commit()
                        session.refresh(new_address)
                        new_places = Places(
                            name=travel.palaces.name,
                            address_id=new_address.id
                        )
                        session.add(new_places)
                        session.commit()
                        session.refresh(new_places)
                        new_comments = Comments(
                            user_id=exist_author.id,
                            text=travel.comments.text
                        )
                        session.add(new_comments)
                        session.commit()
                        session.refresh(new_comments)
                        new_travel = Travels(
                            name=travel.name,
                            price=travel.price,
                            price_type=travel.price_type,
                            description=travel.description,
                            category_id=new_category.id,
                            palaces_id=new_places.id,
                            comment_id=new_comments.id,
                            discounts=travel.discounts
                        )
                        session.add(new_travel)
                        session.commit()
                        session.refresh(new_travel)
                        return HTTPException(status_code=status.HTTP_201_CREATED, detail="Travel created successfully")
                    else:
                        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Author is not found")


@travel_router.get("/{id}")
def get_travel(id: int):
    travel = session.query(Travels).filter(Travels.id == id).first()
    if not travel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return HTTPException(status_code=status.HTTP_200_OK, detail=travel)
