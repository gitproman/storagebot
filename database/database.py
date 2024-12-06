import pymongo
from config import DB_URI, DB_NAME
import asyncio

# Initialize MongoDB client
dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]
user_data = database['users']

async def add_user(user_id: int):
    try:
        user_data.insert_one({'_id': user_id})
    except Exception as e:
        print(f"Error adding user {user_id}: {e}")

async def present_user(user_id: int):
    try:
        found = user_data.find_one({'_id': user_id})
        return bool(found)
    except Exception as e:
        print(f"Error finding user {user_id}: {e}")
        return False

async def full_userbase():
    try:
        user_docs = user_data.find()
        user_ids = [doc['_id'] for doc in user_docs]
        return user_ids
    except Exception as e:
        print(f"Error retrieving user base: {e}")
        return []

async def del_user(user_id: int):
    try:
        result = user_data.delete_one({'_id': user_id})
        
    except Exception as e:
        print(f"Error deleting user {user_id}: {e}")

