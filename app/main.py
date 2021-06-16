from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from view import channel_search

app = FastAPI()

origins = [
    'http://globlin.io',
    'https://globlin.io',
    'https://dev.report.globlin.io',
    'http://dev.report.globlin.io',
    'http://report.globlin.io',
    'https://report.globlin.io',
    'http://localhost:3000',
    'https://localhost:3000',
    'https://scheduler.globlin.io',
    'http://scheduler.globlin.io',
    'https://dev-scheduler.globlin.io',
    'http://dev-scheduler.globlin.io',
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*", ],
    allow_headers=["*", "Authorization"],
)


app.include_router(channel_search.router)