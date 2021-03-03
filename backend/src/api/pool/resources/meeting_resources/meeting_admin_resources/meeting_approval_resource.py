from src.api.pool.decorators.meeting_decorators.meeting_update_proxies.meeting_admin_update_proxies.meeting_approval_update_proxy import \
    MeetingApprovalUpdateProxy
from src.api.pool.decorators.meeting_decorators.meeting_update_proxies.meeting_admin_update_proxies.periodic_approval_update_proxy import \
    PeriodicApprovalUpdateProxy
from src.api.pool.resources.entities.requests.implement_requests.meeting_requests.meeting_nested_periodic_approval_request import \
    MeetingNestedPeriodicApprovalRequest
from ... import BaseAPI, Resource, Request
from ...authenticated_resources.auth_form_resource import BaseAuthenticatedFormResource, AuthenticatedDecorator


class MeetingApprovalResource(BaseAuthenticatedFormResource):
    def _create_service(self) -> AuthenticatedDecorator:
        return MeetingApprovalUpdateProxy()

    def patch(self, request: Request, *args, **kwargs):
        if request.get('periodic'):
            self._set_service(PeriodicApprovalUpdateProxy())
        return super(MeetingApprovalResource, self).patch(request, *args, **kwargs)


class MeetingApprovalAPI(BaseAPI):
    def _create_resource(self) -> Resource:
        return MeetingApprovalResource()

    PATCH = {
        'request': MeetingNestedPeriodicApprovalRequest
    }
