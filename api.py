from mongo import MongoAPI
from typing import Optional
from fastapi import FastAPI, Request
from pydantic import BaseModel, EmailStr
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class user_data(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


# default sanity tester
@app.get('/hello', response_class=HTMLResponse)
async def hello(request: Request):
    return templates.TemplateResponse('hello.html', {'request': request})


@app.get('/')
async def base():
    return {'Status': 'Up and running!'}


@app.post('/route')
async def insert(user: user_data):
    if user is None or user == {}:
        return {'Error': 'Please provide correct/complete info'}

    response = await MongoAPI().insert(user.dict())
    return response


@app.get('/route')
async def read():
    response = MongoAPI().read_all_items()
    return JSONResponse(response)


@app.put('/route/{id}')
async def update(id):
    if Request.json is None or Request.json == {}:
        return {'Error': 'Please provide data to update'}
    elif id < 0:
        return {'Error': 'Please provide correct id'}

    response = MongoAPI().update(Request.json, id)
    return JSONResponse(response)


@app.delete('/route/{id}')
async def delete(id):
    if id < 0:
        return JSONResponse({'Error': 'Please provide correct item id'})

    response = MongoAPI().delete(id)
    return JSONResponse(response)


# @app.errorhandler(404)
# async def page_not_found(e):
#     return render_template('404.html'), 404


if __name__ == '__main__':
    # Remove port=5000 and debug=True for running
    # the application in production environment
    app.run(debug=True, port=5000, host='0.0.0.0')
    # app.run(host='0.0.0.0')
