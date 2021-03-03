from abc import ABC

from . import BaseModifiedRequest
from ...schemas.post_schema import PostSchema


class PostRequest(BaseModifiedRequest, ABC):
    def _create_schema(self) -> PostSchema:
        pass
