from fastapi import APIRouter
from schemas import AddressModel, PlacesModel, TravelCategoryModel, CommentsModel, TravelsModel
from db.database import Session, ENGINE
from fastapi import HTTPException, status
from db.models import Address, TravelCategory, Travels, Comments, Users, Places


session = Session(bind=ENGINE)
travel_category_router = APIRouter(prefix="/travelcategory")


@travel_category_router.get("/")
async def travel_categories_get():
    travel_categories = session.query(TravelCategory).all()
    return travel_categories


@travel_category_router.post("/")
async def create_travel_category(travel_category: TravelCategoryModel):
    exist_author = session.query(Users).filter(Users.username == travel_category.author).first()
    if exist_author is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    else:
        author_id = exist_author.id
    exist_travel_category = session.query(TravelCategory).filter(TravelCategory.name == travel_category.name).first()
    if exist_travel_category:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Travelcategory already exists")
    else:
        new_category = TravelCategory(
            name=travel_category.name,
            author_id=author_id
        )
        session.add(new_category)
        session.commit()
        session.refresh(new_category)
        return {"message": "TravelCategory successful created", "travel_category": new_category}
