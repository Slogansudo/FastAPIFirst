from fastapi import APIRouter
from schemas import AddressModel, PlacesModel, TravelCategoryModel, CommentsModel, TravelsModel, CheckUserModel
from db.database import Session, ENGINE
from fastapi import HTTPException, status, Depends
from db.models import Address, TravelCategory, Travels, Comments, Users, Places
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

session = Session(bind=ENGINE)
travel_category_router = APIRouter(prefix="/travelcategory")


@travel_category_router.get("/")
async def travel_categories_get(Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    travel_categories = session.query(TravelCategory).all()
    return travel_categories


@travel_category_router.post("/")
async def create_travel_category(travel_category: TravelCategoryModel, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    if exist_user.is_staff:
        exist_author = session.query(Users).filter(Users.username == travel_category.author).first()
        if exist_author is None:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
        else:
            author_id = exist_author.id
        exist_travel_category = session.query(TravelCategory).filter(
            TravelCategory.name == travel_category.name).first()
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
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="It is not possible to view user data for you")


@travel_category_router.get("/{id}")
def get_travel_category(id: int, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_travel_category = session.query(TravelCategory).filter(TravelCategory.id == id).first()
    if not exist_travel_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return HTTPException(status_code=status.HTTP_200_OK, detail=exist_travel_category)


@travel_category_router.put("/{id}")
def update_travel_category(id: int, travel_category: TravelCategoryModel, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    if exist_user.is_staff:
        exist_travel_category = session.query(TravelCategory).filter(TravelCategory.id == id).first()
        if not exist_travel_category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        author = session.query(Users).filter(Users.username == travel_category.author).first()
        if author is None:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
        exist_travel_category.author_id = author.id
        exist_travel_category.name = travel_category.name
        session.commit()
        return HTTPException(status_code=status.HTTP_200_OK, detail="successfully updated")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="It is not possible to view user data for you")


@travel_category_router.delete("/{id}")
def delete_travel_category(id: int, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    if exist_user.is_staff:
        exist_travel_category = session.query(TravelCategory).filter(TravelCategory.id == id).first()
        if not exist_travel_category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        session.delete(exist_travel_category)
        session.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="It is not possible to view user data for you")




@travel_category_router.get("/{id}/author")
async def get_travel_category_author(id: int, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_travel_category = session.query(TravelCategory).filter(TravelCategory.id == id).first()
    if not exist_travel_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    data = {
        "user_id": exist_travel_category.author_id,
        "first_name": exist_travel_category.author.first_name,
        "last_name": exist_travel_category.author.last_name,
        "email": exist_travel_category.author.email,
        "is_active": exist_travel_category.author.is_active,
        "is_staff": exist_travel_category.author.is_staff
    }
    data = jsonable_encoder(data)
    return data
