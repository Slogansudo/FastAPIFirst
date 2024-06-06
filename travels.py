from fastapi import APIRouter
from schemas import AddressModel, PlacesModel, TravelCategoryModel, CommentsModel, TravelsModel
from db.database import Session, ENGINE
from fastapi import HTTPException, status, Depends
from db.models import Address, TravelCategory, Travels, Comments, Users, Places
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

session = Session(bind=ENGINE)
travel_router = APIRouter(prefix='/travel')


@travel_router.get("/")
async def travels_get(Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    travels = session.query(Travels).all()
    return travels


@travel_router.post("/")
async def create_travels(travel: TravelsModel, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    if exist_user.is_staff:
        exist_travel = session.query(Travels).filter(Travels.name == travel.name).first()
        if exist_travel:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Travel is alredy exist")
        else:
            exist_travel_category = session.query(TravelCategory).filter(
                TravelCategory.name == travel.category.name).first()
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
                            return HTTPException(status_code=status.HTTP_201_CREATED,
                                                 detail="Travel created successfully")
                        else:
                            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Author is not found")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="It is not possible to view user data for you")


@travel_router.get("/{id}")
def get_travel(id: int, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    travel = session.query(Travels).filter(Travels.id == id).first()
    if not travel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return HTTPException(status_code=status.HTTP_200_OK, detail=travel)


@travel_router.put("/{id}")
def update_travel(id: int, travel: TravelsModel, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    if exist_user.is_staff:
        exist_travel = session.query(Travels).filter(Travels.id == id).first()
        if not exist_travel:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        exist_category = session.query(TravelCategory).filter(TravelCategory.name == travel.category.name).first()
        if not exist_category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category is not found")
        exist_places = session.query(Places).filter(Places.name == travel.palaces.name).first()
        if not exist_places:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Place is not found")
        exist_user = session.query(Users).filter(Users.username == travel.comments.user).first()
        if not exist_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not exist")
        exist_comment = session.query(Comments).filter(Comments.user_id == exist_user.id).first()
        if not exist_comment:
            new_comment = Comments(
                user_id=exist_user.id,
                text=travel.comments.text
            )
            session.add(new_comment)
            session.commit()
            session.refresh(new_comment)
            exist_travel.name = travel.name
            exist_travel.price = travel.price
            exist_travel.price_type = travel.price_type
            exist_travel.description = travel.description
            exist_travel.category_id = exist_category.id
            exist_travel.palaces_id = exist_places.id
            exist_travel.comments_id = new_comment.id
            session.commit()
            return HTTPException(status_code=status.HTTP_200_OK, detail="Travel successfully updated")

        exist_comment.text = travel.comments.text
        exist_comment.user_id = exist_user.id
        session.commit()

        exist_travel.name = travel.name
        exist_travel.price = travel.price
        exist_travel.price_type = travel.price_type
        exist_travel.description = travel.description
        exist_travel.category_id = exist_category.id
        exist_travel.palaces_id = exist_places.id
        exist_travel.comments_id = exist_comment.id
        session.commit()
        return HTTPException(status_code=status.HTTP_200_OK, detail="Travel successfully updated")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="It is not possible to view user data for you")


@travel_router.delete("/{id}")
async def delete_travel(id: int, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    if exist_user.is_staff:
        exist_travel = session.query(Travels).filter(Travels.id == id).first()
        session.delete(exist_travel)
        session.commit()
        return HTTPException(status_code=status.HTTP_200_OK, detail="Travel successfully deleted")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="It is not possible to view user data for you")


@travel_router.get("/{id}/category")
async def get_category(id: int, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    travel = session.query(Travels).filter(Travels.id == id).first()
    if travel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="travel not found")
    data = {
        "category": {
            "id": travel.category_id,
            "name": travel.travel_category.name,
            "author_id": travel.travel_category.author_id,
            "created_date": travel.travel_category.created_date,
            "updated_date": travel.travel_category.updated_date
        }
    }
    data = jsonable_encoder(data)
    raise HTTPException(status_code=status.HTTP_200_OK, detail=data)


@travel_router.get("/{id}/category/author")
async def get_place(id: int, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    travel = session.query(Travels).filter(Travels.id == id).first()
    if travel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    data = {
        "place": {
            "id": travel.travel_category.author_id,
            "username": travel.travel_category.author.username,
            "email": travel.travel_category.author.email,
            "is_active": travel.travel_category.author.is_active
        }
    }
    data = jsonable_encoder(data)
    raise HTTPException(status_code=status.HTTP_200_OK, detail=data)


@travel_router.get("/{id}/place")
async def get_places(id: int, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    travel = session.query(Travels).filter(Travels.id == id).first()
    if travel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Travel not found")
    data = {
        "place": {
            "id": travel.places.id,
            "name": travel.places.name,
            "rating": travel.places.rating,
            "address": {
                "id": travel.places.address.id,
                "name": travel.places.address.name
            },
            "created_date": travel.places.created_date,
            "updated_date": travel.places.updated_date

        }
    }
    data = jsonable_encoder(data)
    raise HTTPException(status_code=status.HTTP_200_OK, detail=data)


@travel_router.get("/{id}/comments")
async def get_place_comments(id: int, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    travel = session.query(Travels).filter(Travels.id == id).first()
    if travel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Travel not found")
    data = {
        "comment": {
            "id": travel.comments.id,
            "text": travel.comments.text,
            "user": {
                "id": travel.comments.users.id,
                "username": travel.comments.users.username,
                "email": travel.comments.users.email
            },
            "created_date": travel.comments.created_date,
            "updated_date": travel.comments.updated_date
        }
    }
    data = jsonable_encoder(data)
    raise HTTPException(status_code=status.HTTP_200_OK, detail=data)

