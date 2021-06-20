from typing import List
import time

from fastapi import APIRouter, BackgroundTasks

from databases import db
from model import schema
from service.channel_searcher import ChannelSearcher


router = APIRouter(
    tags=["channel_searcher"]
)


@router.get("/")
async def index():
    return {"hello": "world"}


@router.post("/influencer/search", response_model=List[schema.Influencer])
async def search_influencer(params: schema.InfluencerSearcher):
    start = time.time()

    searcher = ChannelSearcher(params=params)
    searcher.search_channel_list()
    searcher.search_video_for_channel_id_list()
    searcher.search_channel_detail()
    try:
        result = searcher.get_channel_details_list()
    except TypeError:
        result = [{
            'channel_title': None,
            "thumbnail_url": None,
            "country": None,
            'subscriber_count': None}]

    do = await searcher.insert_influencer_to_db()
    BackgroundTasks().add_task(do, result)

    duration = time.time() - start
    print(f'{duration=}')
    return result
