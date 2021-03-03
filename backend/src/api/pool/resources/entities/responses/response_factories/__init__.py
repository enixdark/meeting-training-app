from abc import ABC, abstractmethod

from src.api.pool.resources import ResourceResponse


class ResponseFactory(ABC):
    @abstractmethod
    def _create_success_response(self, **kwargs) -> ResourceResponse:
        pass

    @abstractmethod
    def _create_failed_response(self, **kwargs) -> ResourceResponse:
        pass

    @abstractmethod
    def get_response(self, *args, **kwargs) -> ResourceResponse:
        pass
