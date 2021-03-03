from abc import ABC

from . import BaseModifiedRequest
from ...schemas.patch_schema import PatchSchema


class PatchRequest(BaseModifiedRequest, ABC):
    def _create_schema(self) -> PatchSchema:
        pass
