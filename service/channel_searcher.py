from collections import OrderedDict
from math import ceil

from retrying import retry

from service.public_func import (
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

    def __init__(self, keyword: str, region: str, max_subscriber: int, min_subcriber: int):
        self.keyword = keyword
        self.region = region
        self.max_subscriber = max_subscriber
        self.min_subscriber = min_subcriber
        self.__region_code = ChannelSearcher.__region_code_map[region]

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
        searched_channel_id_list = list(OrderedDict.fromkeys(self.__channel_id_container))
        print("searched channel results : ", len(searched_channel_id_list))
        return searched_channel_id_list

    def get_channel_details_list(self):
        searched_channel_details_list = self.__channel_details_container
        print("searched channel results : ", len(searched_channel_details_list))
        return searched_channel_details_list

    @retry
    @check_key_quote
    def search_channel_list(self):
        print("search_channel_list : ", self.get_api_key())
        page_token = " "
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
        return

    @retry
    @check_key_quote
    def search_video_for_channel_id_list(self):
        print("search_video_for_channel_id_list : ", self.get_api_key())
        page_token = " "
        for _ in range(10):
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
        loop_count = ceil(len(self.__channel_id_container)/50)
        count = 0
        for i in range(loop_count):
            ids = self.__channel_id_container[count:count+50]
            search_func = get_channel_details(min_subscriber=self.min_subscriber,
                                              max_subscriber=self.max_subscriber,
                                              developer_key=self.get_api_key(),
                                              channel_ids_container=ids,
                                              metadata_container=self.__channel_details_container)
            count += 50
        return self.__channel_details_container

    def insert_influencer_to_db(self):
        col = db['influencer']
        x = col.insert_many(self.__channel_details_container)
        print(x.inserted_ids)
        return


a = ChannelSearcher(keyword="김치 먹방", region="한국", min_subcriber=100000, max_subscriber=10000000000)

a.search_channel_list()
a.search_video_for_channel_id_list()
print(a.get_channel_id_list())
c = a.search_channel_detail()
print(a.get_channel_details_list())
a.insert_influencer_to_db()