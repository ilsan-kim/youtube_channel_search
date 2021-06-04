from collections import OrderedDict

from googleapiclient.errors import HttpError

from service.public_func import (
    get_id_list
)
from service.decorator_func import check_key_quote
from service.key_changer import KeySelector


class ChannelSearcher():
    __key_selector = KeySelector()
    __channel_id_container = []
    __region_code_map = {
        "한국": "KR",
        "일본": "US",
        "미국": "US",
        "캐나다": "CA",
        "영국": "GB",
        "프랑스": "FR"
    }

    def __init__(self, keyword: str, region: str):
        self.keyword = keyword
        self.region = region
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

    @check_key_quote
    def search_channel_list(self):
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

    @check_key_quote
    def search_video_for_channel_id_list(self):
        page_token = " "
        for _ in range(6):
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

a = ChannelSearcher(keyword="산천어 축제", region="한국")

a.search_channel_list()
a.search_video_for_channel_id_list()
print(a.get_channel_id_list())
