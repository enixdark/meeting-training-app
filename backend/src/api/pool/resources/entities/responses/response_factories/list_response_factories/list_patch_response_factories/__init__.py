from abc import ABC, abstractmethod

from src.api.pool.resources.entities.responses.implement_responses.method_responses.update_responses import \
    ResourceUpdateResponse
from .. import ListResponseFactory


class ListPatchResponseFactory(ListResponseFactory, ABC):
    @abstractmethod
    def _create_success_response(self, success: int, **kwargs) -> ResourceUpdateResponse:
        pass

    @abstractmethod
    def _create_failed_response(self, failed: int, **kwargs) -> ResourceUpdateResponse:
        pass

    @abstractmethod
    def _create_partial_response(self, success: int, failed: int, *args, **kwargs) -> ResourceUpdateResponse:
        pass
