from abc import ABC

from . import BaseModifiedRequest
from ...schemas.delete_schema import DeleteSchema


class DeleteRequest(BaseModifiedRequest, ABC):
    def _create_schema(self) -> DeleteSchema:
        pass
