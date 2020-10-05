import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

db_connection = os.environ.get('DB_CONNECTION')
mongo_username = os.environ.get('MONGODB_USER')
mongo_password = os.environ.get('MONGODB_PASS')
mongo_database = os.environ.get('MONGO_DB_NAME')


class MongoAPI:
    def __init__(self):
        self.client = MongoClient(
            'mongodb://{}:27017/'.format(db_connection),
            username='{}'.format(mongo_username),
            password='{}'.format(mongo_password))

        database = '{}'.format(mongo_database)
        collection = '{}-collection'.format(mongo_database)
        cursor = self.client[database]
        self.collection = cursor[collection]

    async def insert(self, data: dict):
        _response = self.collection.insert_one(data)
        _user = self.collection.find_one({'_id': _response.inserted_id})
        return {
            'user': '{}'.format(_user),
            'statuscode': 200
        }

    async def read_item(self, id: str):
        _user = self.collection.find_one({'_id': ObjectId(id)})
        if _user:
            return {
                'user': '{}'.format(_user),
                'statuscode': 200
            }
        else:
            return {
                'message': 'User with ID: {} does not exist'.format(id),
                'statuscode': 404
            }

    async def read_all_items(self):
        _users = []
        for item in self.collection.find():
            _users.append(item)
        if _users:
            return {
                'users': '{}'.format(_users),
                'statuscode': 200
            }
        else:
            return {
                'message': 'No User exist in the DB',
                'statuscode': 404
            }

    async def update(self, id: str, data: dict):
        _user = self.collection.find_one({'_id': ObjectId(id)})
        if _user:
            updated_user = self.collection.update_one(
                    {'_id': ObjectId(id)}, {'$set': data})
            if updated_user:
                return {
                    'user': '{}'.format(id),
                    'statuscode': 204
                }
        else:
            return {
                'message': 'User ID does not exist.',
                'statuscode': 404
            }

    async def delete(self, id: str):
        _user = self.collection.find_one({'_id': ObjectId(id)})
        if _user:
            self.collection.delete_one({'_id': ObjectId(id)})
            return {
                'message': 'Item deleted successfully',
                'statuscode': 204
            }
        else:
            return {
                'message': 'User ID does not exist.',
                'statuscode': 404
            }
