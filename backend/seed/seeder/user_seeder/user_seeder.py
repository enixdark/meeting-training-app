from abc import ABC

from seed.seeder import Seeder
from src.api.pool.services import FormService
from src.api.pool.services.user_services import UserFormService


class UserSeeder(Seeder, ABC):
    def _create_form_service(self) -> FormService:
        return UserFormService()
