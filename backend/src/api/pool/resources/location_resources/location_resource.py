from src.api.pool.resources import Resource, BaseAPI
from src.api.pool.resources.form_resource import FormService
from src.api.pool.services.location_services import LocationInstantFormService
from ..base_resource import BaseResource
from ..entities.requests.implement_requests.location_requests import LocationGetRequest, LocationPostRequest, \
    LocationPatchRequest


class LocationResource(BaseResource):
    def _create_service(self) -> FormService:
        return LocationInstantFormService()


class LocationAPI(BaseAPI):
    def _create_resource(self) -> Resource:
        return LocationResource()

    GET = {
        'request': LocationGetRequest
    }

    POST = {
        'request': LocationPostRequest
    }

    PATCH = {
        'request': LocationPatchRequest
    }

    DELETE = {
        'request': None
    }
