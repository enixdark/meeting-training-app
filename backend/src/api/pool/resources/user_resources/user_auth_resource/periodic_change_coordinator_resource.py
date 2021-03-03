from src.api.pool.resources.entities.responses.implement_responses.method_responses.update_responses import ListUpdateFailedResponse, \
    ListUpdateSuccessResponse, ListUpdatePartialResponse
from src.api.pool.decorators.attendee_decorators.change_coordinator_decorator.periodic_change_coordinator_decorator import \
    PeriodicChangeCoordinatorDecorator
from ... import BaseAPI, Resource
from ...authenticated_resources.auth_resource import BaseAuthenticatedResource, AuthenticatedDecorator, Request
from ...entities.requests.implement_requests.attendee_requests.change_coordinator_request import \
    AttendeeCoordinatorRequest
from src.api.pool.resources.entities.responses.implement_responses.method_responses.update_responses.change_coordinator_responses import CoordinatorUpdateSuccessResponse


class PeriodicChangeCoordinatorResource(BaseAuthenticatedResource):
    def _create_service(self) -> AuthenticatedDecorator:
        return PeriodicChangeCoordinatorDecorator()

    def patch(self, request: Request, *args, **kwargs):
        # set authentication to the authenticated service
        self._set_up_authenticate_service(request)
        if isinstance(self._service, PeriodicChangeCoordinatorDecorator):
            self._service.update_model(**request.all())
            self._set_response(CoordinatorUpdateSuccessResponse())

        success = self._service.get_success_count()
        failed = self._service.get_failed_count()
        message = self._service.get_periodic_messages()

        if success == 0:
            self._set_response(ListUpdateFailedResponse(failed=failed, success=0))
        elif failed == 0:
            self._set_response(ListUpdateSuccessResponse(failed=0, success=success))
        else:
            self._set_response(ListUpdatePartialResponse(failed=failed, success=success))
        return message


class PeriodicChangeCoordinatorAuthAPI(BaseAPI):
    def _create_resource(self) -> Resource:
        return PeriodicChangeCoordinatorResource()

    PATCH = {
        'request': AttendeeCoordinatorRequest
    }
