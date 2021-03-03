from seed.composite_seeder import SeederComposite
from seed.seeder.location_seeder.update_location_manager_seeder import UpdateLocationManagerSeeder
from seed.seeder.location_seeder.update_location_seeder import UpdateLocationSeeder


class UpdateLocationComposite(SeederComposite):
    def _create_seeder_list(self) -> list:
        return [
            UpdateLocationSeeder,
            UpdateLocationManagerSeeder
        ]
