
from fastapi import APIRouter
from schemas import RegisterModel, LoginModel
from db.database import Session, ENGINE
from fastapi import HTTPException, status
from db.models import Users
from werkzeug import security


session = Session(bind=ENGINE)
auth_router = APIRouter(prefix="/auth")


@auth_router.get("/users")
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


@auth_router.get("/users/{id}")
async def get_user(id: int):
    data = session.query(Users).filter(Users.id == id).first()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    form = {
        'id': data.id,
        'first_name': data.first_name,
        'last_name': data.last_name,
        'username': data.username,
        'email': data.email,
        'password': '*****',
        'is_staff': data.is_staff,
        'is_active': data.is_active,
    }
    return form


@auth_router.put("/users/{id}")
async def update_user(id: int, update_user: RegisterModel):
    user = session.query(Users).filter(Users.id == id).first()
    if user:
        search = session.query(Users).filter(Users.username == update_user.username).first()
        if not search or search.username == user.username:
            user.username = update_user.username
        else:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="such a user exists")
        user.email = update_user.email
        search = session.query(Users).filter(Users.email == update_user.email).first()
        if not search or search.email == user.email:
            user.email = update_user.email
        else:
            return HTTPException(status_code=400, detail="such a user's email exists")
        user.password = update_user.password
        user.first_name = update_user.first_name
        user.last_name = update_user.last_name
        session.commit()
        session.refresh(user)
        return HTTPException(status_code=status.HTTP_200_OK, detail="user successful updated")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@auth_router.delete("/users/{id}")
async def delete_user(id: int):
    user = session.query(Users).filter(Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        session.delete(user)
        session.commit()
        return HTTPException(status_code=status.HTTP_508_LOOP_DETECTED, detail="user successfully deleted")

@auth_router.get("/")
async def auth():
    return {"message": "THIS IS THE AUTH PAGE"}


@auth_router.get("/login")
async def login():
    return {"message": "THIS IS LOGIN PAGE"}


@auth_router.post("/login")
async def new_login(user: LoginModel):
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
async def new_register(user: RegisterModel):
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

