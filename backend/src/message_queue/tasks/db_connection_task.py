from config import WebApiConfig
from src.api.pool.services import BaseService
from src.database import PostgresConnector
from . import BaseMeetingTask, abstractmethod


class DBConnectionTask(BaseMeetingTask):
    session = None
    service = None

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    @abstractmethod
    def _create_service(self) -> BaseService:
        pass

    def _prepared_service(self, base_service=None) -> BaseService:
        if not base_service:
            base_service = self._create_service()
        base_service.session = self._get_session
        return base_service

    @property
    def _get_session(self):
        if not self.session:
            db = PostgresConnector(WebApiConfig.DATABASE_URI)
            self.session = db.get_session()
        return self.session

    @property
    def _get_service(self) -> BaseService:
        return self.service

    def close_session(self):
        self.session.close()

    def commit_session(self):
        self.session.commit()

    def rollback_session(self):
        self.session.rollback()
