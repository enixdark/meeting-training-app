from abc import ABC, abstractmethod

from src.api.pool.decorators.auth_decorator import AuthenticatedDecorator
from src.api.pool.services import Service


class Proxy(AuthenticatedDecorator, ABC):
    @abstractmethod
    def _check_authorization(self, *args, **kwargs) -> bool:
        pass

    @abstractmethod
    def _create_service(self) -> Service:
        pass
