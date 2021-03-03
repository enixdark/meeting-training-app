from src.api.pool.decorators.meeting_decorators.meeting_update_proxies.meeting_admin_update_proxies.meeting_admin_update_proxy import \
    MeetingAdminUpdateProxy
from src.api.pool.proxies.admin_proxies.admin_create_proxies.admin_meeting_create_proxy import AdminEmailCreateProxy
from src.api.pool.proxies.admin_proxies.admin_create_proxies.admin_periodic_create_proxy import \
    AdminPeriodicMeetingCreateProxy
from src.api.pool.resources.entities.requests.implement_requests.meeting_requests.meeting_nested_periodic_request import \
    MeetingPeriodicNestedPostRequest
from ... import BaseAPI, Resource, Request
from ...authenticated_resources.auth_form_resource import BaseAuthenticatedFormResource, AuthenticatedDecorator
from ...entities.requests.implement_requests.meeting_requests.meeting_nested_requests import MeetingNestedPatchRequest


class MeetingAdminPatchResource(BaseAuthenticatedFormResource):
    def _create_service(self) -> AuthenticatedDecorator:
        return MeetingAdminUpdateProxy()

    def post(self, request: Request, *args, **kwargs):
        if request.get('periodic'):
            self._set_service(AdminPeriodicMeetingCreateProxy())
        else:
            self._set_service(AdminEmailCreateProxy())
        return super(MeetingAdminPatchResource, self).post(request, *args, **kwargs)


class MeetingAdminPatchAPI(BaseAPI):
    def _create_resource(self) -> Resource:
        return MeetingAdminPatchResource()

    PATCH = {
        'request': MeetingNestedPatchRequest
    }

    POST = {
        'request': MeetingPeriodicNestedPostRequest
    }
