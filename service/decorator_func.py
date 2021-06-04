from googleapiclient.errors import HttpError


def check_key_quote(method):
    def wrapper(self):
        try:
            method(self)
        except HttpError:
            print("API_KEY error")
            self.change_api_key()
            method(self)
    return wrapper