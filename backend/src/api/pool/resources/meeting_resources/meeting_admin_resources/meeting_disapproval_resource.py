from src.api.pool.decorators.meeting_decorators.meeting_update_proxies.meeting_admin_update_proxies.meeting_disapproval_update_proxy import \
    MeetingDisapprovalUpdateProxy
from src.api.pool.decorators.meeting_decorators.meeting_update_proxies.meeting_admin_update_proxies.periodic_disapproval_update_proxy import \
    PeriodicDisapprovalUpdateProxy
from src.api.pool.proxies.admin_proxies.admin_delete_proxies.admin_meeting_delete_proxy import \
    AdminMeetingDeleteDecorator
from src.api.pool.resources.entities.requests.implement_requests.meeting_requests.meeting_nested_periodic_approval_request import \
    MeetingNestedPeriodicApprovalRequest
from ... import BaseAPI, Resource, Request
from ...authenticated_resources.auth_form_resource import BaseAuthenticatedFormResource, AuthenticatedDecorator
from ...entities.requests.implement_requests.meeting_requests.meeting_nested_requests import MeetingNestedPatchRequest, \
    MeetingNestedDeleteRequest


class MeetingDisapprovalResource(BaseAuthenticatedFormResource):
    def _create_service(self) -> AuthenticatedDecorator:
        return MeetingDisapprovalUpdateProxy()

    def delete(self, request: Request, *args, **kwargs):
        self._set_service(AdminMeetingDeleteDecorator())
        return super(MeetingDisapprovalResource, self).delete(request, *args, **kwargs)

    def patch(self, request: Request, *args, **kwargs):
        if request.get('periodic'):
            self._set_service(PeriodicDisapprovalUpdateProxy())
        return super(MeetingDisapprovalResource, self).patch(request, *args, **kwargs)


class MeetingDisapprovalAPI(BaseAPI):
    def _create_resource(self) -> Resource:
        return MeetingDisapprovalResource()

    PATCH = {
        'request': MeetingNestedPeriodicApprovalRequest
    }

    DELETE = {
        'request': MeetingNestedDeleteRequest
    }
