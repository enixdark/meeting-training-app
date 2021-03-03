from abc import ABC, abstractmethod

from src.api.pool.resources.entities.responses.implement_responses.method_responses.get_responses import \
    ResourceGetResponse
from src.api.pool.resources.entities.responses.response_factories import ResponseFactory


class SingleResponseFactory(ResponseFactory, ABC):
    @abstractmethod
    def _create_success_response(self, **kwargs) -> ResourceGetResponse:
        pass

    @abstractmethod
    def _create_failed_response(self, **kwargs) -> ResourceGetResponse:
        pass

    def get_response(self, is_success: bool, *args, **kwargs) -> ResourceGetResponse:
        if is_success:
            return self._create_success_response()
        else:
            return self._create_failed_response()
