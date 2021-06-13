import os
from dotenv import load_dotenv

from pymongo import MongoClient

load_dotenv(".env")

client = MongoClient(os.environ['MONGODB_URL'])
print(os.environ['MONGODB_URL'])

db = client.college
