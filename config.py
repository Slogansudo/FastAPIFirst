from fastapi import FastAPI
from auth import auth_router
from travels import travel_router
from travel_category import travel_category_router
from places import places_router
from comments import comments_router
from addresses import address_router
from fastapi_jwt_auth import AuthJWT
from schemas import JwtModel

app = FastAPI(title="FastAPI v1")


@AuthJWT.load_config
def get_config():
    return JwtModel()


app.include_router(auth_router, prefix="/api/v1")
app.include_router(travel_router, prefix="/api/v1")
app.include_router(travel_category_router, prefix="/api/v1")
app.include_router(places_router, prefix="/api/v1")
app.include_router(comments_router, prefix="/api/v1")
app.include_router(address_router, prefix="/api/v1")


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
