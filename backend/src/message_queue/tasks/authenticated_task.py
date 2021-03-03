from src.api.pool.services import BaseService
from src.api.pool.services.user_services import UserFormService
from src.database.postgres.user import User
from src.message_queue.tasks.db_connection_task import DBConnectionTask


class AuthenticatedTask(DBConnectionTask):
    auth_user = None

    def run(self, *args, **kwargs):
        pass

    def _create_service(self) -> BaseService:
        return UserFormService()

    def _retrieve_authenticated_user(self, user_id: int) -> User:
        user_service = self._prepared_service(base_service=UserFormService())
        auth_user = user_service.get_model(_id=user_id)
        if isinstance(auth_user, User):
            return auth_user
