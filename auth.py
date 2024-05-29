
from fastapi import APIRouter
from schemas import RegisterModel
from db.database import Session, ENGINE
from fastapi import HTTPException, status
from db.models import Users, Address, TravelCategory, Travels, Comments
from werkzeug import security


session = Session(bind=ENGINE)
auth_router = APIRouter(prefix="/auth")


@auth_router.get("/")
async def auth():
    return {"message": "THIS IS THE AUTH PAGE"}


@auth_router.get("/login")
async def login():
    return {"message": "THIS IS LOGIN PAGE"}


@auth_router.get('/register')
async def register():
    return {'message': 'welcome to Register page '}


@auth_router.post('/register')
async def register(user: RegisterModel):
    username = session.query(Users).filter(Users.username == user.username).first()
    if username:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday foydalanuvchi allaqachon mavjud")
    email = session.query(Users).filter(Users.email == user.email).first()

    if email:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday bunday email allaqachon mavjud")

    new_user = Users(
        id=user.id,
        username=user.username,
        email=user.email,
        password=security.generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active,
    )
    session.add(new_user)
    session.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED,)

