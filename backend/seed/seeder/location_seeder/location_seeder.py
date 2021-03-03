from abc import ABC

from seed.seeder import Seeder
from src.api.pool.services import FormService
from src.api.pool.services.location_services import LocationFormService


class LocationSeeder(Seeder, ABC):
    def _create_form_service(self, service=LocationFormService()) -> FormService:
        return service
