from seed.composite_seeder import SeederComposite
from seed.seeder.location_seeder.update_location_manager_seeder import UpdateLocationManagerSeeder
from seed.seeder.user_seeder.update_user_role_seeder import UpdateUserRoleSeeder


class UpdateRoleComposite(SeederComposite):
    def _create_seeder_list(self) -> list:
        return [
            UpdateUserRoleSeeder,
            UpdateLocationManagerSeeder
        ]
