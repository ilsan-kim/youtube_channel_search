from typing import Optional

from pydantic import Field, BaseModel
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Influencer(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    channel_title: str
    thumbnail_url: str
    country: str
    subscriber_count: int

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class InfluencerSearcher(BaseModel):
    keyword: str
    region: str
    max_subscriber: int
    min_subscriber: int

    class Config:
        orm_mode = True
