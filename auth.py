
from fastapi import APIRouter


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
