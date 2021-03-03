from abc import ABC, abstractmethod

from .. import BaseSchemaRequest, request


class BaseGetRequest(BaseSchemaRequest, ABC):

    def _get_raw_data(self) -> dict:
        return {
            'id': self.__get_id(),
            'limit': self.__get_limit(),
            'offset': self.__get_offset(),
            'sort': self.__get_sort(),
            'order': self.__get_order(),
            'relations': self.__get_relations(),
            **self.filter_rules()
        }

    def __get_id(self):
        _id = self._get_url_parameter('id')
        if _id:
            return _id
        return 0

    def __get_limit(self):
        limit = self._get_url_parameter('limit')
        if limit:
            return limit
        return 20

    def __get_offset(self):
        offset = self._get_url_parameter('offset')
        if offset:
            return offset
        return 0

    def __get_sort(self):
        sort = self._get_url_parameter('sort')
        if sort:
            return sort
        return 'id'

    def __get_order(self):
        order = self._get_url_parameter('order')
        if order:
            return order
        return 'asc'

    def __get_relations(self):
        relations = self._get_url_list_parameter('relations')
        if relations:
            return relations
        return []

    @staticmethod
    def _get_url_parameter(key: str):
        return request.args.get(key)

    @staticmethod
    def _get_url_list_parameter(key: str):
        return request.args.getlist('{}[]'.format(key))

    @abstractmethod
    def filter_rules(self) -> dict:
        pass
