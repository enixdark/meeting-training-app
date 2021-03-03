from abc import ABC

from .. import BaseSchemaRequest, request


class BaseModifiedRequest(BaseSchemaRequest, ABC):
    def _get_raw_data(self) -> dict:
        return request.get_json()

    @staticmethod
    def _get_url_parameter(key: str):
        return request.args.get(key)

    @staticmethod
    def _get_url_list_parameter(key: str):
        return request.args.getlist('{}[]'.format(key))
