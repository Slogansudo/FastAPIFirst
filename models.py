from fastapi import APIRouter

model_router = APIRouter(prefix='/models')


@model_router.get('/')
async def get_models():
    return {"message": "This is models page"}


@model_router.get('/1')
async def model1():
    return {'message': 'This is model 1 page'}


@model_router.post('/2')
async def model2():
    return {'message': 'This is model 2 page'}


@model_router.get('/3')
async def model3():
    return {'message': 'This is model 3 page'}
