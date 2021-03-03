from src.api.pool.services.user_services import UserFormService
from . import locations
from .location_seeder import LocationSeeder


class UpdateLocationManagerSeeder(LocationSeeder):
    def _seed(self):
        location_service = self._get_service()
        user_service = UserFormService()
        user_service.session = self._get_session()

        manager = user_service.find_model(pairs={'email': 'quyetnguyencr7@gmail.com'})

        for location in locations:
            current_location = location_service.find_model(
                pairs={'google_map_id': location['google_map_id']}
            )
            if current_location:
                location_service.update_model(_id=current_location.id, manager=manager)
