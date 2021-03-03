from seed.seeder.user_seeder.user_seeder import UserSeeder
from src.api.pool.services.role_services import RoleFormService


class UpdateUserRoleSeeder(UserSeeder):
    def _seed(self):
        user_service = self._get_service()
        admin = user_service.find_model(pairs={'email': 'quyetnguyencr7@gmail.com'})
        role_service = RoleFormService()
        role_service.session = self._get_session()
        admin.roles = role_service.get_all()
