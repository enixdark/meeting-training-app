from abc import ABC, abstractmethod

from src.api.pool.services import FormService


class Seeder(ABC):
    def __init__(self, session):
        self.__service = self._create_form_service()
        self.__session = session
        pass

    @abstractmethod
    def _create_form_service(self) -> FormService:
        pass

    @abstractmethod
    def _seed(self):
        pass

    def run(self):
        self.__before_seeding()
        self._seed()
        self.__after_seeding()

    def close_session(self):
        if self.__service.session:
            self.__service.session.close()

    def __before_seeding(self):
        self.__service.session = self.__session

    def __after_seeding(self):
        if self.__service:
            self.__service.session.commit()

    def _set_service(self, service: FormService):
        self.__service = service
        self.__before_seeding()

    def _get_service(self) -> FormService:
        return self.__service

    def _remove_all_model(self):
        current_models = self.__service.get_all()
        for current_model in current_models:
            self.__service.delete_model(_id=current_model.id)
        self.__service.session.commit()

    def _get_session(self):
        return self.__session