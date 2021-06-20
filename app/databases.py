import os
from dotenv import load_dotenv

import motor.motor_asyncio
from pymongo import MongoClient

load_dotenv(".env")

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ['MONGODB_URL'])
# client = MongoClient(os.environ['MONGODB_URL'])
print(os.environ['MONGODB_URL'])

db = client.college

# db = client.youtube_searcher
# collection = client.search_result
