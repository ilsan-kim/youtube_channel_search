import time

from googleapiclient.errors import HttpError


def check_key_quote(method):
    def wrapper(self):
        try:
            method(self)
        except HttpError:
            prev_key = self.get_api_key()
            print("API_KEY error")
            self.change_api_key()
            new_key = self.get_api_key()
            print('previous key : {} -> new key : {}'.format(prev_key, new_key))
    return wrapper