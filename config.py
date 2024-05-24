from fastapi import FastAPI
from auth import auth_router, login_router, register_router
from models import model_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(login_router)
app.include_router(register_router)
app.include_router(model_router)


@app.get("/")
async def index():
    return {"message": "Hello world"}


@app.get("/test")
async def index2():
    return {"message": "this students page"}
