from fastapi import FastAPI

from view import channel_search

app = FastAPI()

app.include_router(channel_search.router)