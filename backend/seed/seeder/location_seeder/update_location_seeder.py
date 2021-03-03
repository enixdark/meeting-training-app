from . import locations
from .location_seeder import LocationSeeder


class UpdateLocationSeeder(LocationSeeder):
    def _seed(self):
        location_service = self._get_service()
        for location in locations:
            current_location = location_service.find_model(
                pairs={'google_map_id': location['google_map_id']}
            )
            if current_location:
                location_service.update_model(_id=current_location.id, **location)
            else:
                location_service.create_new_model(**location)
