import os
from dotenv import load_dotenv

import motor.motor_asyncio
from pymongo import MongoClient

load_dotenv(".env")

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get('MONGODB_URL', 'mongodb://localhost:27017/'))
# client = MongoClient(os.environ['MONGODB_URL'])
print(os.environ.get('MONGODB_URL', 'mongodb://localhost:27017/'))

db = client.college

# db = client.youtube_searcher
# collection = client.search_result
