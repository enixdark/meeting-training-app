from src.database.postgres.location import Location
from src.api.pool.services import FormService, DecoratorService, InstantFormService


class LocationFormService(FormService):
    def _create_class_model(self):
        return Location


class LocationInstantFormService(InstantFormService):
    def _create_class_model(self):
        return Location


class LocationDecoratorService(DecoratorService):
    def _create_class_model(self):
        return Location
