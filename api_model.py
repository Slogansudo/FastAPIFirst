from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.get("/")
async def read_items():
    return {"massage": 'Hello World!'}


@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item


@app.get("/items/")
async def read_item() -> list:
    # return [
    #     Item(name="Peter", price=5.99),
    #     Item(name="John", price=32.0)
    # ]
    return [
        {
            'name': 'Peter',
            'password': '1234'
        },
        {
            'name': 'John',
            'password': '2134'
        },
        {
            'name': 'Marko',
            'password': 'mark2312'
        },
    ]


@app.get("/products/")
async def read_product() -> list[Item]:
    return [
        Item(name="Peter", price=5.99),
        Item(name="Jack", price=20),
        Item(name="John", price=32.0)
    ]


@app.get("/users/")
async def users() -> list:
    return [
        {
            'username': 'Peter',
            'password': '3243',
            'email': 'example@gmail.com'
        },
        {
            'username': 'Jack',
            'password': '2145',
            'email': 'example@gmail.com'
        },
        {
            'username': 'Marko',
            'password': 'srm',
            'email': 'example@gmail.com'
        }
    ]


@app.get("/comments/")
async def read_comments() -> list:
    return [
        {
            'user': 'sardor',
            'text': 'This is a test comment'
        },
        {
            'user': 'salim',
            'text': 'This is a Login page '
        }
    ]


@app.get("/places/")
async def read_places() -> list:
    return [
        {
            'name': 'New York city',
            'city': 'New York ',
            'price': 234
        },
        {
            'name': 'San Francisco',
            'city': 'San Francisco',
            'price': 345
        }
    ]


@app.post("/producs/")
async def create_product(item: Item) -> Item:
    return item


@app.post("/users/")
async def create_user(item: Item) -> Item:
    return item
