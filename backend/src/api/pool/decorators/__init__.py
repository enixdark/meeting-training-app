from abc import ABC, abstractmethod

from src.database.postgres.base import Model
from src.api.pool.services import Service, BaseService


class Decorator(Service, ABC):
    def __init__(self):
        self.__service = self._create_service()

    @abstractmethod
    def _create_service(self) -> BaseService:
        pass

    def create_new_model(self, *args, **kwargs) -> Model:
        return self.__service.create_new_model(*args, **kwargs)

    def update_model(self, *args, **kwargs) -> bool:
        return self.__service.update_model(*args, **kwargs)

    def find_model(self, pairs: dict, **kwargs) -> Model:
        return self.__service.find_model(pairs, **kwargs)

    def delete_model(self, *args, **kwargs) -> bool:
        return self.__service.delete_model(*args, **kwargs)

    def get_model(self, _id, **kwargs) -> Model:
        return self.__service.get_model(_id, **kwargs)

    def get_all(self, *args, **kwargs):
        return self.__service.get_all(*args, **kwargs)

    def set_service(self, service: Service):
        self.__service = service

    def _get_service(self):
        return self.__service


class SessionManager(ABC):
    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def add_to_session(self, data):
        pass

    @abstractmethod
    def remove_from_session(self, data):
        pass

    @abstractmethod
    def rollback(self):
        pass


class BaseDecorator(Decorator, SessionManager, ABC):
    def commit(self):
        service = self._get_service()
        try:
            service.session.commit()
        except Exception as e:
            print(e)
            service.session.rollback()

    def add_to_session(self, model: Model):
        service = self._get_service()
        service.session.add(model)

    def remove_from_session(self, model: Model):
        service = self._get_service()
        service.session.delete(model)

    def rollback(self):
        service = self._get_service()
        service.session.rollback()
