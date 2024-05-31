from fastapi import APIRouter
from schemas import AddressModel, PlacesModel, TravelCategoryModel, CommentsModel, TravelsModel
from db.database import Session, ENGINE
from fastapi import HTTPException, status
from db.models import Address, TravelCategory, Travels, Comments, Users, Places


session = Session(bind=ENGINE)
api_router = APIRouter(prefix='/api/v1')


@api_router.get('/users')
async def get_users():
    data1 = session.query(Users).all()
    data = []
    for i in data1:
        if i.is_active != True:
            form = {
                'username': i.username,
                'email': i.email,
                'password': '*****',
                'is_staff': i.is_staff,
                'is_active': i.is_active,
            }
            data.append(form)
    return data


@api_router.get("/address")
async def address():
    addresses = session.query(Address).all()
    return addresses


@api_router.post("/address")
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


@api_router.get("/places")
async def get_places():
    places = session.query(Places).all()
    return places


@api_router.post("/places")
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


@api_router.get("/TravelCategories")
async def travel_categories_get():
    travel_categories = session.query(TravelCategory).all()
    return travel_categories


@api_router.post("/TravelCategories")
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


@api_router.get("/comments")
async def comments_get():
    comments = session.query(Comments).all()
    return comments


@api_router.post("/comments")
async def create_comment(comments: CommentsModel):
    exist_user = session.query(Users).filter(Users.username == comments.user).first()
    if exist_user:
        new_comment = Comments(
            user_id=exist_user.id,
            text=comments.text,
        )
        session.add(new_comment)
        session.commit()
        session.refresh(new_comment)
        return HTTPException(status_code=status.HTTP_201_CREATED, detail=new_comment)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")


@api_router.get("/travels")
async def travels_get():
    travels = session.query(Travels).all()
    return travels


@api_router.post("/travels")
async def create_travels(travel: TravelsModel):
    exists_travel = session.query(Travels).filter(Travels.name == travel.name).first()
    if exists_travel:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This travel already exists")
    exist_category = session.query(TravelCategory).filter(TravelCategory.name == travel.category.name)
    category_id = exist_category.id
    if exist_category:
        exist_address = session.query(Address).filter(Address.name == travel.palaces.address.name).first()
        exist_places = session.query(Places).filter(Places.name == travel.palaces.name).first()
        if exist_address and exist_places:
            exist_places.address_id = exist_address.id
            session.add(exist_places)
            session.commit()
            session.refresh(exist_places)
            exist_user = session.query(Users).filter(Users.username == travel.comments.user).first()
            if exist_user:
                new_comment = Comments(
                    user_id=exist_user.id,
                    text=travel.comments.text,
                )
                session.add(new_comment)
                session.commit()
                session.refresh(new_comment)
                new_travel = Travels(
                    name=travel.name,
                    price=travel.price,
                    price_type=travel.price_type,
                    description=travel.description,
                    category_id=category_id,
                    palaces_id=exist_places.id,
                    comment_id=new_comment.id,
                    discounts=travel.discounts
                )
                session.add(new_travel)
                session.commit()
                session.refresh(new_travel)

                return HTTPException(status_code=status.HTTP_201_CREATED, detail=new_travel)
            else:
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
        elif not exist_places and exist_address:
            new_places = Places(
                name=travel.palaces.name,
                address_id=exist_address.id
            )
            session.add(new_places)
            session.commit()
            session.refresh(new_places)
            exist_user = session.query(Users).filter(Users.username == travel.comments.user).first()
            if exist_user:
                new_comment = Comments(
                    user_id=exist_user.id,
                    text=travel.comments.text,
                )
                session.add(new_comment)
                session.commit()
                session.refresh(new_comment)
                new_travel = Travels(
                    name=travel.name,
                    price=travel.price,
                    price_type=travel.price_type,
                    description=travel.description,
                    category_id=category_id,
                    palaces_id=new_places.id,
                    comment_id=new_comment.id,
                    discounts=travel.discounts
                )
                session.add(new_travel)
                session.commit()
                session.refresh(new_travel)
                return HTTPException(status_code=status.HTTP_201_CREATED, detail=new_travel)
            else:
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
        elif exist_places and not exist_address:
            new_address = Address(
                name=travel.palaces.address.name,
            )
            session.add(new_address)
            session.commit()
            session.refresh(new_address)
            exist_places.address_id = new_address.id
            session.add(exist_places)
            session.commit()
            session.refresh(exist_places)
            exist_user = session.query(Users).filter(Users.username == travel.comments.user).first()
            if exist_user:
                new_comment = Comments(
                    user_id=exist_user.id,
                    text=travel.comments.text,
                )
                session.add(new_comment)
                session.commit()
                session.refresh(new_comment)
                new_travel = Travels(
                    name=travel.name,
                    price=travel.price,
                    price_type=travel.price_type,
                    description=travel.description,
                    category_id=category_id,
                    palaces_id=exist_places.id,
                    comment_id=new_comment.id,
                    discounts=travel.discounts
                )
                session.add(new_travel)
                session.commit()
                session.refresh(new_travel)
                return HTTPException(status_code=status.HTTP_201_CREATED, detail=new_travel)
            else:
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
        elif not exist_places and not exist_address:
            new_address = Address(
                name=travel.palaces.address.name,
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
            exist_user = session.query(Users).filter(Users.username == travel.comments.user).first()
            if exist_user:
                new_comment = Comments(
                    user_id=exist_user.id,
                    text=travel.comments.text,
                )
                session.add(new_comment)
                session.commit()
                session.refresh(new_comment)
                new_travel = Travels(
                    name=travel.name,
                    price=travel.price,
                    price_type=travel.price_type,
                    description=travel.description,
                    category_id=category_id,
                    palaces_id=exist_places.id,
                    comment_id=new_comment.id,
                    discounts=travel.discounts
                )
                session.add(new_travel)
                session.commit()
                session.refresh(new_travel)
                return HTTPException(status_code=status.HTTP_201_CREATED, detail=new_travel)
            else:
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    else:
        author = session.query(Users).filter(Users.username == travel.category.author).first()
        if author:
            new_category = TravelCategory(
                author_id=author.id,
                name=travel.category.name
            )
            session.add(new_category)
            session.commit()
            session.refresh(new_category)
            exist_address = session.query(Address).filter(Address.name == travel.palaces.address.name).first()
            exist_places = session.query(Places).filter(Places.name == travel.palaces.name).first()
            if exist_address and exist_places:
                exist_places.address_id = exist_address.id
                session.add(exist_places)
                session.commit()
                session.refresh(exist_places)
                exist_user = session.query(Users).filter(Users.username == travel.comments.user).first()
                if exist_user:
                    new_comment = Comments(
                        user_id=exist_user.id,
                        text=travel.comments.text,
                    )
                    session.add(new_comment)
                    session.commit()
                    session.refresh(new_comment)
                    new_travel = Travels(
                        name=travel.name,
                        price=travel.price,
                        price_type=travel.price_type,
                        description=travel.description,
                        category_id=category_id,
                        palaces_id=exist_places.id,
                        comment_id=new_comment.id,
                        discounts=travel.discounts
                    )
                    session.add(new_travel)
                    session.commit()
                    session.refresh(new_travel)

                    return HTTPException(status_code=status.HTTP_201_CREATED, detail=new_travel)
                else:
                    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
            elif not exist_places and exist_address:
                new_places = Places(
                    name=travel.palaces.name,
                    address_id=exist_address.id
                )
                session.add(new_places)
                session.commit()
                session.refresh(new_places)
                exist_user = session.query(Users).filter(Users.username == travel.comments.user).first()
                if exist_user:
                    new_comment = Comments(
                        user_id=exist_user.id,
                        text=travel.comments.text,
                    )
                    session.add(new_comment)
                    session.commit()
                    session.refresh(new_comment)
                    new_travel = Travels(
                        name=travel.name,
                        price=travel.price,
                        price_type=travel.price_type,
                        description=travel.description,
                        category_id=category_id,
                        palaces_id=new_places.id,
                        comment_id=new_comment.id,
                        discounts=travel.discounts
                    )
                    session.add(new_travel)
                    session.commit()
                    session.refresh(new_travel)
                    return HTTPException(status_code=status.HTTP_201_CREATED, detail=new_travel)
                else:
                    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
            elif exist_places and not exist_address:
                new_address = Address(
                    name=travel.palaces.address.name,
                )
                session.add(new_address)
                session.commit()
                session.refresh(new_address)
                exist_places.address_id = new_address.id
                session.add(exist_places)
                session.commit()
                session.refresh(exist_places)
                exist_user = session.query(Users).filter(Users.username == travel.comments.user).first()
                if exist_user:
                    new_comment = Comments(
                        user_id=exist_user.id,
                        text=travel.comments.text,
                    )
                    session.add(new_comment)
                    session.commit()
                    session.refresh(new_comment)
                    new_travel = Travels(
                        name=travel.name,
                        price=travel.price,
                        price_type=travel.price_type,
                        description=travel.description,
                        category_id=category_id,
                        palaces_id=exist_places.id,
                        comment_id=new_comment.id,
                        discounts=travel.discounts
                    )
                    session.add(new_travel)
                    session.commit()
                    session.refresh(new_travel)
                    return HTTPException(status_code=status.HTTP_201_CREATED, detail=new_travel)
                else:
                    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
            elif not exist_places and not exist_address:
                new_address = Address(
                    name=travel.palaces.address.name,
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
                exist_user = session.query(Users).filter(Users.username == travel.comments.user).first()
                if exist_user:
                    new_comment = Comments(
                        user_id=exist_user.id,
                        text=travel.comments.text,
                    )
                    session.add(new_comment)
                    session.commit()
                    session.refresh(new_comment)
                    new_travel = Travels(
                        name=travel.name,
                        price=travel.price,
                        price_type=travel.price_type,
                        description=travel.description,
                        category_id=category_id,
                        palaces_id=exist_places.id,
                        comment_id=new_comment.id,
                        discounts=travel.discounts
                    )
                    session.add(new_travel)
                    session.commit()
                    session.refresh(new_travel)
                    return HTTPException(status_code=status.HTTP_201_CREATED, detail=new_travel)
                else:
                    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
        else:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")