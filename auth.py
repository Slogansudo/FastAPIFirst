
from fastapi import APIRouter
from schemas import RegisterModel, LoginModel
from db.database import Session, ENGINE
from fastapi import HTTPException, status
from db.models import Users
from werkzeug import security


session = Session(bind=ENGINE)
auth_router = APIRouter(prefix="/auth")


@auth_router.get("/")
async def auth():
    return {"message": "THIS IS THE AUTH PAGE"}


@auth_router.get("/login")
async def login():
    return {"message": "THIS IS LOGIN PAGE"}


@auth_router.post("/login")
async def login(user: LoginModel):
    username = session.query(Users).filter(Users.username == user.username).first()
    user_check = session.query(Users).filter(Users.username == user.username).first()
    if username:
        if username and security.check_password_hash(user_check.password, user.password):
            return HTTPException(status_code=status.HTTP_200_OK, detail="Successful")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="username yoki password xato")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="bunday foydalanuvchi topilmadi")


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
        username=user.username,
        email=user.email,
        password=security.generate_password_hash(user.password),
    )
    session.add(new_user)
    session.commit()
    data = {'username': new_user.username, 'email': new_user.email, "is_active": new_user.is_active}
    return HTTPException(status_code=status.HTTP_201_CREATED, detail=data)

