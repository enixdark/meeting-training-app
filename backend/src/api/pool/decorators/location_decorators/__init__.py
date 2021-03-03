from src.api.pool.services.location_services import LocationFormService
from src.api.pool.decorators import BaseDecorator, Service


class LocationDecorator(BaseDecorator):
    def _create_service(self) -> Service:
        return LocationFormService()

    def _get_service(self) -> LocationFormService:
        return super()._get_service()
