from seed.composite_seeder import SeederComposite
from seed.seeder.location_seeder.init_location_seeder import InitLocationSeeder
from seed.seeder.role_seeder.init_role_seeder import InitRoleSeeder


class InitSeederComposite(SeederComposite):
    def _create_seeder_list(self) -> list:
        return [
            InitLocationSeeder,
            InitRoleSeeder
        ]
