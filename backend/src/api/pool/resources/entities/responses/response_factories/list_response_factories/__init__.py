from abc import ABC, abstractmethod

from src.api.pool.resources import ResourceResponse
from src.api.pool.resources.entities.responses.response_factories import ResponseFactory


class ListResponseFactory(ResponseFactory, ABC):
    @abstractmethod
    def _create_success_response(self, success: int, **kwargs) -> ResourceResponse:
        pass

    @abstractmethod
    def _create_failed_response(self, failed: int, **kwargs) -> ResourceResponse:
        pass

    @abstractmethod
    def _create_partial_response(self, success: int, failed: int, **kwargs) -> ResourceResponse:
        pass

    def get_response(self, success: int, failed: int, *args, **kwargs) -> ResourceResponse:
        if success == 0:
            return self._create_failed_response(failed)
        elif failed == 0:
            return self._create_success_response(success)
        else:
            return self._create_partial_response(success=success, failed=failed)
