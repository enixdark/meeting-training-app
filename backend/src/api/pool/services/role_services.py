from src.database.postgres.role import Role
from src.api.pool.services import FormService, InstantFormService


class RoleFormService(FormService):

    def create_many_to_many_relations(self) -> dict:
        return {'users': 'users'}

    def _create_class_model(self):
        return Role


class RoleInstantFormService(InstantFormService):
    def _create_class_model(self):
        return Role
