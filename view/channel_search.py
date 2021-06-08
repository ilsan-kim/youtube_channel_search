from typing import List

from fastapi import APIRouter

from model import schema
from service.channel_searcher import ChannelSearcher

router = APIRouter(
    tags=["channel_searcher"]
)

@router.get("/index")
async def index():
    return {"hello": "world"}


@router.post("/influencer/search", response_model=List[schema.Influencer])
async def search_influencer(params: schema.InfluencerSearcher):
    searcher = ChannelSearcher(params=params)
    searcher.search_channel_list()
    searcher.search_video_for_channel_id_list()
    searcher.search_channel_detail()
    searcher.insert_influencer_to_db()
    try:
        result = searcher.get_channel_details_list()
    except TypeError:
        result = [{
            'channel_title': None,
            "thumbnail_url": None,
            "country": None,
            'subscriber_count': None}]

    return result

