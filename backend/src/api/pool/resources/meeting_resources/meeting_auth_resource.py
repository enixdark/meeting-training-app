from src.api.pool.decorators.meeting_decorators.meeting_celery_decorators.meeting_calendar_task_decorator.meeting_calendar_create_decorators.period_meeting_calendar_create_decorator import \
    PeriodicMeetingCalendarCreateDecorator
from src.api.pool.decorators.meeting_decorators.meeting_celery_decorators.meeting_email_task_decorator.meeting_email_approval_create_decorator import \
    MeetingEmailApprovalCreateDecorator
from src.api.pool.decorators.meeting_decorators.meeting_update_proxies.meeting_coordinator_update_proxies.meeting_coordinator_update_proxy import \
    MeetingCoordinatorUpdateProxy
from src.api.pool.proxies.meeting_coordinator_proxies.coordinator_delete_proxies.coordinator_meeting_delete_proxy import \
    CoordinatorMeetingDeleteDecorator
from .. import BaseAPI, Resource, Request
from ..authenticated_resources.auth_form_resource import BaseAuthenticatedFormResource, \
    AuthenticatedDecorator
from ..entities.requests.implement_requests.meeting_requests.meeting_nested_periodic_request import \
    MeetingPeriodicNestedPostRequest
from ..entities.requests.implement_requests.meeting_requests.meeting_nested_requests import MeetingNestedPatchRequest, \
    MeetingNestedDeleteRequest


class MeetingAuthResource(BaseAuthenticatedFormResource):
    def _create_service(self) -> AuthenticatedDecorator:
        return MeetingCoordinatorUpdateProxy()

    def post(self, request: Request, *args, **kwargs):
        if request.get('periodic'):
            self._set_service(PeriodicMeetingCalendarCreateDecorator())
        else:
            self._set_service(MeetingEmailApprovalCreateDecorator())
        return super().post(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        self._set_service(CoordinatorMeetingDeleteDecorator())
        return super(MeetingAuthResource, self).delete(request, *args, **kwargs)


class MeetingAuthAPI(BaseAPI):
    def _create_resource(self) -> Resource:
        return MeetingAuthResource()

    PATCH = {
        'request': MeetingNestedPatchRequest
    }

    DELETE = {
        'request': MeetingNestedDeleteRequest
    }

    POST = {
        'request': MeetingPeriodicNestedPostRequest
    }
