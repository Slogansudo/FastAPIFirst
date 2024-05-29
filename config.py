from fastapi import FastAPI
from auth import auth_router
#from db.models import model_router

app = FastAPI()
app.include_router(auth_router)

@app.get("/")
async def index():
    return {"message": "Hello world"}


@app.get("/product/{id}")
async def indexing(id: int):
    return {"message": f"Product - {id} "}


@app.post("/product")
async def post_product():
    return {"message": "This is POST page"}

@app.post("/test")
async def index2():
    return {"message": "this students POST page"}
