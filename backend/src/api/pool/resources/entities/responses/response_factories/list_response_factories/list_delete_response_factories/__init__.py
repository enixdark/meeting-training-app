from abc import ABC, abstractmethod

from src.api.pool.resources.entities.responses.implement_responses.method_responses.delete_responses import \
    ResourceDeleteResponse, ListDeletePartialResponse, ListDeleteSuccessResponse, ListDeleteFailedResponse
from src.api.pool.resources.entities.responses.response_factories.list_response_factories import ListResponseFactory


class ListDeleteResponseFactories(ListResponseFactory, ABC):
    @abstractmethod
    def _create_success_response(self,  success: int, **kwargs) -> ResourceDeleteResponse:
        pass

    @abstractmethod
    def _create_failed_response(self, failed: int, **kwargs) -> ResourceDeleteResponse:
        pass

    @abstractmethod
    def _create_partial_response(self, success: int, failed: int, **kwargs) -> ResourceDeleteResponse:
        pass
