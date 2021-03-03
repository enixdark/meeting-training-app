from abc import ABC, abstractmethod

from src.api.pool.resources.entities.responses.implement_responses.method_responses.create_responses import \
    ResourceCreateResponse
from .. import ListResponseFactory


class ListPostResponseFactory(ListResponseFactory, ABC):
    @abstractmethod
    def _create_success_response(self, success: int, **kwargs) -> ResourceCreateResponse:
        pass

    @abstractmethod
    def _create_failed_response(self, failed: int, **kwargs) -> ResourceCreateResponse:
        pass

    @abstractmethod
    def _create_partial_response(self, success: int, failed: int, *args, **kwargs) -> ResourceCreateResponse:
        pass
