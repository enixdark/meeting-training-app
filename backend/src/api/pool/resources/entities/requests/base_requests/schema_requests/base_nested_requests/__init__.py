from abc import ABC, abstractmethod

from ..base_modified_requests import BaseModifiedRequest
from ...schemas.nested_schemas import NestedSchema


class BaseNestedModifyRequest(BaseModifiedRequest, ABC):
    def _get_raw_data(self) -> dict:
        raw_data = super()._get_raw_data()
        if isinstance(raw_data, list):
            if len(raw_data) > 0:
                for item in raw_data:
                    if not isinstance(item, dict):
                        break
                else:
                    return {'nested': raw_data}
        return {}

    @abstractmethod
    def _create_schema(self) -> NestedSchema:
        pass

    def get_nested_data(self) -> list:
        return self.get('nested')


class NestedPostRequest(BaseNestedModifyRequest, ABC):
    pass


class NestedPatchRequest(BaseNestedModifyRequest, ABC):
    pass


class NestedDeleteRequest(BaseNestedModifyRequest, ABC):
    pass
