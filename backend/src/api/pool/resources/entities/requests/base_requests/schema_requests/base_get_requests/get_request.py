from abc import ABC, abstractmethod

from . import BaseGetRequest
from ...schemas.get_schema import GetSchema


class GetRequest(BaseGetRequest, ABC):
    @abstractmethod
    def _create_schema(self) -> GetSchema:
        pass
