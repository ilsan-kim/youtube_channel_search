class KeySelector():
    # API Key List
    __API_KEY = {
        3: "AIzaSyCmOvTsBo_g__NBVQtCOrUQEmbR1KlRcds",
        2: "AIzaSyC93iswqAWhnEW8M7WJX96IGSYBCCUUZis",
        5: "AIzaSyA48pQnfHZ8ka43eraiJNWDzuzCmLzgWGw",
        4: "AIzaSyAjOoFpidz5Qt_BEGbku_tcEXpVhIfxZcg",
        1: "AIzaSyCWHsYAjaXbgalCvWyg6UVlhS4RwwNY3sU"
    }
    API_KEY_COUNTER = 1

    @classmethod
    def change_api_key(cls):
        '''
        쿼리 후 새로운 API키를 할당하기 위한 메서드로, 쿼리를 위한 유튜브 API 통신 객체 선언 전 사용해줘야 함
        :return:
        '''
        if cls.API_KEY_COUNTER < len(cls.__API_KEY):
            pre_key = cls.__API_KEY[cls.API_KEY_COUNTER]
            cls.API_KEY_COUNTER += 1
            after_key = cls.__API_KEY[cls.API_KEY_COUNTER]
            return "change api key [from : {}] [to : {}]".format(pre_key, after_key)
        elif cls.API_KEY_COUNTER == len(cls.__API_KEY):
            pre_key = cls.__API_KEY[cls.API_KEY_COUNTER]
            cls.API_KEY_COUNTER = 1
            after_key = cls.__API_KEY[cls.API_KEY_COUNTER]
            return "change api key [from : {}] [to : {}]".format(pre_key, after_key)

    def get_api_key(self):
        return self.__API_KEY[self.API_KEY_COUNTER]
