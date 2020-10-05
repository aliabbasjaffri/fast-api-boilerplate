from typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

    class Config:
        schema_extra = {
            'example': {
                'username': 'johndoe',
                'email': 'doe@john.com',
                'full_name': 'John Doe'
            }
        }


def responseMessage(message: str, statuscode: str, data: Optional[dict] = None):
    response = {}
    response['message'] = message
    response['statuscode'] = statuscode
    if data is not None:
        response['data'] = data
    return response
