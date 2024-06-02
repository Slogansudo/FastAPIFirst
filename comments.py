from fastapi import APIRouter
from schemas import AddressModel, PlacesModel, TravelCategoryModel, CommentsModel, TravelsModel
from db.database import Session, ENGINE
from fastapi import HTTPException, status
from db.models import Address, TravelCategory, Travels, Comments, Users, Places

comments_router = APIRouter(prefix="/comments")
session = Session(bind=ENGINE)


@comments_router.get("/")
async def comments_get():
    comments = session.query(Comments).all()
    return comments


@comments_router.post("/")
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


@comments_router.get("/{id}")
async def read_comment(id: int):
    comment = session.query(Comments).filter(Comments.id == id).first()
    if comment:
        return HTTPException(status_code=status.HTTP_200_OK, detail=comment)
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@comments_router.put("/{id}")
async def update_comment(id: int, comment: CommentsModel):
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
