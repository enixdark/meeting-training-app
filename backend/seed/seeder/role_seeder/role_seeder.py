from abc import ABC

from seed.seeder import Seeder
from src.api.pool.services import FormService
from src.api.pool.services.role_services import RoleFormService


class RoleSeeder(Seeder, ABC):
    def _create_form_service(self) -> FormService:
        return RoleFormService()
