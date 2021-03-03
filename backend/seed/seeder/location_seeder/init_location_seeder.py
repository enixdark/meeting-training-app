from . import locations
from .location_seeder import LocationSeeder


class InitLocationSeeder(LocationSeeder):
    def _seed(self):
        location_service = self._get_service()
        for location in locations:
            location_service.create_new_model(**location)
