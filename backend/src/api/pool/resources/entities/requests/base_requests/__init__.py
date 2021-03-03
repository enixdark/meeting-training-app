from abc import ABC

from .. import Request


class BaseRequest(Request, ABC):
    def __init__(self, authentication: dict):
        self.__data = {}
        self.__header = {}
        self.__method = None
        self.__authentication = authentication

    def all(self) -> dict:
        return self.__data

    def get(self, keyword):
        return self.__data.get(keyword, None)

    def header(self, name=''):
        if len(name) > 0:
            return self.__header.get(name, None)
        return self.__header

    def method(self):
        return self.__method

    def _set_data(self, data: dict, header: dict, method):
        self.__data = data
        self.__header = header
        self.__method = method

    def get_authentication(self):
        return self.__authentication
