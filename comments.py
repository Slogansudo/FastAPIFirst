from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from schemas import AddressModel, PlacesModel, TravelCategoryModel, CommentsModel, TravelsModel
from db.database import Session, ENGINE
from fastapi import HTTPException, status, Depends
from db.models import Address, TravelCategory, Travels, Comments, Users, Places
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

comments_router = APIRouter(prefix="/comments")
session = Session(bind=ENGINE)


@comments_router.get("/")
async def comments_get(Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    comments = session.query(Comments).all()
    return comments


@comments_router.post("/")
async def create_comment(comments: CommentsModel, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
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


@comments_router.get("/{id}")
async def read_comment(id: int, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    comment = session.query(Comments).filter(Comments.id == id).first()
    if comment:
        return HTTPException(status_code=status.HTTP_200_OK, detail=comment)
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@comments_router.put("/{id}")
async def update_comment(id: int, comment: CommentsModel, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    commentw = session.query(Comments).filter(Comments.id == id).first()
    if not commentw:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    users = session.query(Users).filter(Users.username == comment.user).first()
    if not users:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    commentw.user_id = users.id
    commentw.text = comment.text
    session.commit()
    return HTTPException(status_code=status.HTTP_200_OK, detail=comment)


@comments_router.delete("/{id}")
async def delete_comment(id: int, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    exist_user = session.query(Users).filter(Users.username == Authentization.get_jwt_subject()).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist")
    if exist_user.is_staff:
        comment = session.query(Comments).filter(Comments.id == id).first()
        if not comment:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        session.delete(comment)
        session.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="It is not possible to view user data for you")


@comments_router.get("/{id}/about_comment")
async def active_users(id: int, Authentization: AuthJWT = Depends()):
    try:
        Authentization.jwt_required()
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    comments = session.query(Comments).filter(Comments.id == id).first()
    if not comments:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    comments.reads_count += 1
    session.commit()
    data = {
        "text": comments.text,
        "reads_count": comments.reads_count,
        "user": {
            comments.users.username,
            comments.users.first_name,
            comments.users.last_name,
            comments.users.is_active
        },
        "create_date": comments.created_date,
        "last_update": comments.updated_date,
    }
    return jsonable_encoder(data)

