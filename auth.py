from fastapi import APIRouter


auth_router = APIRouter(prefix="/auth")
login_router = APIRouter(prefix="/login")
register_router = APIRouter(prefix="/register")


@auth_router.get("/")
async def auth():
    return {"message": "THIS IS THE AUTH PAGE"}


@login_router.get("/")
async def login():
    return {"message": "THIS IS LOGIN PAGE"}


@register_router.get('/')
async def register():
    return {'message': 'welcome to Register page '}
