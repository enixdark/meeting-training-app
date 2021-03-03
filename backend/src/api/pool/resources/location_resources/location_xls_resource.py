from src.api.pool.decorators.auth_decorator import AuthenticatedDecorator
from src.api.pool.decorators.location_decorators.location_xls_decorator import LocationXLSDecorator
from src.api.pool.resources import BaseAPI, Resource, Request
from src.api.pool.resources.authenticated_resources.auth_form_resource import BaseAuthenticatedFormResource
from src.api.pool.resources.entities.requests.base_requests.schema_requests.base_nested_requests import \
    NestedPostRequest
from src.api.pool.resources.entities.requests.implement_requests.location_requests.nested_location_xls_request import \
    NestedLocationXLSRequest


class LocationXLSResource(BaseAuthenticatedFormResource):
    def _create_service(self) -> AuthenticatedDecorator:
        return LocationXLSDecorator()

    def post(self, request: Request, *args, **kwargs):
        if isinstance(request, NestedPostRequest):
            if isinstance(self._service, LocationXLSDecorator):
                self._set_up_authenticate_service(request)
                self._service.get_all(**request.all())
                response_factory = self._create_post_response_factory()
                self._set_response(response_factory.get_response(failed=self._service.get_failed_count(),
                                                                 success=self._service.get_success_count()))
                return self._service.get_xls_messages()


class LocationXLSAPI(BaseAPI):
    def _create_resource(self) -> Resource:
        return LocationXLSResource()

    POST = {
        'request': NestedLocationXLSRequest
    }
