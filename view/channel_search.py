from fastapi import APIRouter

router = APIRouter(
    tags=["channel_searcher"]
)

@router.get("/index")
async def index():
    return {"hello": "world"}
