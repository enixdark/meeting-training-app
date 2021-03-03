from src.api.pool.services.location_services import LocationFormService
from .. import Resource, Service, Request, BaseAPI
from ..entities.requests.implement_requests.location_requests import LocationGetRequest
from src.api.pool.resources.entities.responses.implement_responses.method_responses.get_responses.location_get_responses import LocationListResourceResponse, \
    LocationListErrorResourceResponse


class ListLocationResource(Resource):
    def _create_service(self) -> Service:
        return LocationFormService()

    def get(self, request: Request, *args, **kwargs):
        locations = self._service.get_all(**request.all())
        if len(locations) > 0:
            self._set_response(LocationListResourceResponse())
            relations = request.get('relations')
            return [location.serialize(inclusion_rs=relations) for location in locations]
        self._set_response(LocationListErrorResourceResponse())
        return []


class ListLocationAPI(BaseAPI):
    def _create_resource(self) -> Resource:
        return ListLocationResource()

    GET = {
        'request': LocationGetRequest
    }
