from src.api.pool.decorators.attendee_decorators.change_coordinator_decorator import ChangeCoordinatorDecorator
from ... import BaseAPI, Resource
from ...authenticated_resources.auth_resource import BaseAuthenticatedResource, AuthenticatedDecorator, Request
from ...entities.requests.implement_requests.attendee_requests.change_coordinator_request import \
    AttendeeCoordinatorRequest
from src.api.pool.resources.entities.responses.implement_responses.method_responses.update_responses.change_coordinator_responses import CoordinatorUpdateSuccessResponse


class ChangeCoordinatorResource(BaseAuthenticatedResource):
    def _create_service(self) -> AuthenticatedDecorator:
        return ChangeCoordinatorDecorator()

    def patch(self, request: Request, *args, **kwargs):
        # set authentication to the authenticated service
        self._set_up_authenticate_service(request)

        updated = self._service.update_model(**request.all())
        self._set_response(CoordinatorUpdateSuccessResponse())

        return [updated]


class ChangeCoordinatorAuthAPI(BaseAPI):
    def _create_resource(self) -> Resource:
        return ChangeCoordinatorResource()

    PATCH = {
        'request': AttendeeCoordinatorRequest
    }
