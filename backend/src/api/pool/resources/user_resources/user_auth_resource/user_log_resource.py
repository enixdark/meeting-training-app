from src.api.pool.resources.entities.requests.implement_requests.attendee_requests.log_meeting_request import \
    AttendeeLogRequest
from src.api.pool.resources.entities.responses.implement_responses.method_responses.get_responses.attendee_log_responses import AttendeeLogResourceResponse
from src.api.pool.decorators.attendee_decorators.log_decorator import AttendeeLogDecorator
from ... import BaseAPI, Resource, Request
from ...authenticated_resources.auth_resource import BaseAuthenticatedResource, AuthenticatedDecorator


class AttendeeLogResource(BaseAuthenticatedResource):
    def _create_service(self) -> AuthenticatedDecorator:
        return AttendeeLogDecorator()

    def get(self, request: Request, *args, **kwargs):
        self._set_up_authenticate_service(request=request)
        self._set_response(AttendeeLogResourceResponse())
        return self._service.get_all(**request.all())


class AttendeeLogAuthAPI(BaseAPI):
    def _create_resource(self) -> Resource:
        return AttendeeLogResource()

    GET = {
        'request': AttendeeLogRequest
    }
