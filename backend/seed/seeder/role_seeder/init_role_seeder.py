from . import roles
from .role_seeder import RoleSeeder


class InitRoleSeeder(RoleSeeder):
    def _seed(self):
        role_service = self._get_service()
        for role in roles:
            role_service.create_new_model(**role)
