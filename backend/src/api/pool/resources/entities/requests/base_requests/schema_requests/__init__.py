from abc import ABC, abstractmethod

from flask import request
from marshmallow import Schema, ValidationError

from .. import BaseRequest


class BaseSchemaRequest(BaseRequest, ABC):
    def __init__(self, authentication: dict):
        super().__init__(authentication)
        self.__schema = self._create_schema()
        self.__init_request_data(authentication)

    @abstractmethod
    def _create_schema(self) -> Schema:
        pass

    @staticmethod
    def __load_header() -> dict:
        # print('header', request.headers)
        return request.headers

    @staticmethod
    def __load_method() -> str:
        # print('method', request.method)
        return request.method

    def __load_data(self) -> dict:
        raw_data = self._get_raw_data()
        # print('raw data', raw_data)
        deserialize = self.__schema.load(raw_data)
        if len(deserialize.errors) > 0:
            raise ValidationError(deserialize.errors)
        return deserialize.data

    @abstractmethod
    def _get_raw_data(self) -> dict:
        pass

    def _set_schema(self, schema: Schema):
        self.__schema = schema

    def __init_request_data(self, authentication):
        if len(authentication) > 0:
            self._set_data(self.__load_data(), self.__load_header(), self.__load_method())
        else:
            self._set_data({}, self.__load_header(), None)
