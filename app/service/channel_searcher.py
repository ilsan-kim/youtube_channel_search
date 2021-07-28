from collections import OrderedDict
from math import ceil

from retrying import retry

from service.search_func import (
    get_id_list, get_channel_details
)
from service.decorator_func import check_key_quote
from service.key_changer import KeySelector
from model import schema
from databases import db


class ChannelSearcher():
    db = db
    __key_selector = KeySelector()
    __channel_id_container = []
    __channel_details_container = []
    __region_code_map = {
        "한국": "KR",
        "일본": "US",
        "미국": "US",
        "캐나다": "CA",
        "영국": "GB",
        "프랑스": "FR"
    }

    def __init__(self, params: schema.InfluencerSearcher):
        self.keyword = params.keyword
        self.region = params.region
        self.max_subscriber = params.max_subscriber
        self.min_subscriber = params.min_subscriber
        self.__region_code = ChannelSearcher.__region_code_map[params.region]

    def __str__(self):
        return "Youtube Searcher : keyword={}, region={} (code={})".\
            format(self.keyword, self.region, self.__region_code)

    @classmethod
    def get_api_key(cls):
        return cls.__key_selector.get_api_key()

    @classmethod
    def change_api_key(cls):
        return cls.__key_selector.change_api_key()

    def get_region_code(self):
        return self.__region_code

    def get_channel_id_list(self):
        self.__channel_id_container = list(OrderedDict.fromkeys(self.__channel_id_container))
        return self.__channel_id_container

    def get_channel_details_list(self):
        searched_channel_details_list = self.__channel_details_container
        print("searched channel results : ", len(searched_channel_details_list))
        return searched_channel_details_list

    @retry
    @check_key_quote
    def search_channel_list(self):
        print("search_channel_list : ", self.get_api_key())
        page_token = " "
        count = 0
        while page_token:
            print(page_token)
            search_func = get_id_list(keyword=self.keyword,
                                      region_code=self.__region_code,
                                      developer_key=self.get_api_key(),
                                      page_token=page_token,
                                      type="channel",
                                      container=self.__channel_id_container)
            page_token = search_func["next_page_token"]
            print(len(self.__channel_id_container))
            count += 1
            # 검색량 늘리려면 여기 수정
            if count == 3 or page_token is None:
                break
        return

    @retry
    @check_key_quote
    def search_video_for_channel_id_list(self):
        print("search_video_for_channel_id_list : ", self.get_api_key())
        page_token = " "
        # 검색량 늘리려면 여기 수정
        for _ in range(3):
            print(page_token)
            search_func = get_id_list(keyword=self.keyword,
                                      region_code=self.__region_code,
                                      developer_key=self.get_api_key(),
                                      page_token=page_token,
                                      type="video",
                                      container=self.__channel_id_container)
            page_token = search_func["next_page_token"]
            print(len(self.__channel_id_container))
        return

    @retry
    @check_key_quote
    def search_channel_detail(self):
        print("search_channel_detail : ", self.get_api_key())
        # 중복 제거
        self.get_channel_id_list()

        loop_count = ceil(len(self.__channel_id_container)/50)
        count = 0
        for i in range(loop_count):
            ids = self.__channel_id_container[count:count+50]
            search_func = get_channel_details(keyword=self.keyword,
                                              min_subscriber=self.min_subscriber,
                                              max_subscriber=self.max_subscriber,
                                              developer_key=self.get_api_key(),
                                              channel_ids_container=ids,
                                              metadata_container=self.__channel_details_container)
            count += 50
        return self.__channel_details_container

    async def insert_influencer_to_db(self):
        col = db['influencer']
        try:
            await col.insert_many(self.__channel_details_container)
        except TypeError:
            print("No data to insert")
        return
