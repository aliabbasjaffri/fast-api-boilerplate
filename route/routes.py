from mongo import MongoAPI
from fastapi import APIRouter, Request
from model.user import User, responseMessage
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse


router = APIRouter()
templates = Jinja2Templates(directory='templates')


# default sanity tester
@router.get('/hello', response_class=HTMLResponse)
async def hello(request: Request):
    return templates.TemplateResponse('hello.html', {'request': request})


@router.get('/', response_class=JSONResponse)
async def base():
    return responseMessage('Up and running!', '200')


@router.post('/route', response_class=JSONResponse)
async def insert(user: User):
    if user is None or user == {}:
        return responseMessage('Please provide correct/complete info', '422')
    _user = await MongoAPI().insert(user.dict())
    return responseMessage(
        'User added.',
        '200',
        '{}'.format(_user)
    )


@router.get('/route/{id}', response_class=JSONResponse)
async def read(id: str):
    _user = await MongoAPI().read_item(id)
    return responseMessage(
        'User fetched.',
        '200',
        '{}'.format(_user)
    )


@router.get('/route', response_class=JSONResponse)
async def readAll():
    _users = await MongoAPI().read_all_items()
    return responseMessage(
        'Users fetched.',
        '200',
        '{}'.format(_users)
    )


@router.put('/route/{id}', response_class=JSONResponse)
async def update(id: str, user: User):
    if user is None or user == {}:
        return responseMessage('Please provide correct/complete info', '422')
    elif id is None:
        return responseMessage('Please provide correct id', '422')
    _data = await MongoAPI().update(id, user.dict())
    if _data['user']:
        return responseMessage(
            'User updated.',
            '{}'.format(_data['statuscode']),
            'User with ID: {} updated.'.format(_data['user'])
        )
    else:
        return responseMessage(
            '{}'.format(_data['message']),
            '{}'.format(_data['statuscode'])
        )


@router.delete('/route/{id}', response_class=JSONResponse)
async def delete(id: str):
    if id is None:
        return responseMessage('Please provide correct item id', '422')
    _response = await MongoAPI().delete(id)
    return responseMessage(
            '{}'.format(_response['message']),
            '{}'.format(_response['statuscode'])
        )
