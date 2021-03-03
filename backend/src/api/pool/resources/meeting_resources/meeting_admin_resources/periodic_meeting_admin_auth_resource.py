from src.api.pool.decorators.auth_decorator import AuthenticatedDecorator
from src.api.pool.decorators.meeting_decorators.meeting_update_proxies.meeting_admin_update_proxies.periodic_meeting_admin_update_proxy import \
    PeriodicMeetingAdminUpdateProxy
from src.api.pool.resources import BaseAPI, Resource
from src.api.pool.resources.authenticated_resources.auth_resource import BaseAuthenticatedResource, Request
from src.api.pool.resources.entities.requests.implement_requests.meeting_requests.periodic_meeting_patch_request import \
    PeriodicMeetingPatchRequest
from src.api.pool.resources.entities.responses.implement_responses.method_responses.update_responses import \
    ListUpdateFailedResponse, ListUpdateSuccessResponse, ListUpdatePartialResponse


class PeriodicMeetingAdminPatchResource(BaseAuthenticatedResource):
    def _create_service(self) -> AuthenticatedDecorator:
        return PeriodicMeetingAdminUpdateProxy()

    def patch(self, request: Request, *args, **kwargs):
        if isinstance(self._service, PeriodicMeetingAdminUpdateProxy):
            # set auth user to auth service
            self._set_up_authenticate_service(request=request)

            # update multiple periodic meetings related to periodic meeting with input id
            request_data = request.all()
            _id = request_data.pop('id')
            self._service.update_model(_id=_id, **request_data)

            periodic_service = self._service.get_periodic_update_service()
            success = periodic_service.get_success_count()
            failed = periodic_service.get_failed_count()
            message = periodic_service.get_periodic_messages()

            if success == 0:
                self._set_response(ListUpdateFailedResponse(failed=failed))
            elif failed == 0:
                self._set_response(ListUpdateSuccessResponse(success=success))
            else:
                self._set_response(ListUpdatePartialResponse(failed=failed, success=success))
            return message


class PeriodicMeetingAdminPatchAPI(BaseAPI):
    def _create_resource(self) -> Resource:
        return PeriodicMeetingAdminPatchResource()

    PATCH = {
        'request': PeriodicMeetingPatchRequest
    }
