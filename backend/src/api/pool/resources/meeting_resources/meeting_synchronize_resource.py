from abc import ABC

from src.api.pool.decorators.meeting_decorators.meeting_update_decorators.meeting_synchronize_decorator import \
    MeetingSynchronizeDecorator
from .. import Resource, Service, BaseAPI, Request
from ..authenticated_resources.auth_resource import BaseAuthenticatedResource
from ..entities.requests.implement_requests.meeting_requests.meeting_synchronize_request import \
    MeetingSynchronizedRequest
from src.api.pool.resources.entities.responses.implement_responses.method_responses.update_responses.synchronized_responses import \
    MeetingSynchronizedSuccessResponse, MeetingNotSynchronizedResponse


class MeetingSynchronizeResource(BaseAuthenticatedResource, ABC):
    def _create_service(self) -> Service:
        return MeetingSynchronizeDecorator()

    def patch(self, request: Request, *args, **kwargs):
        self._set_up_authenticate_service(request)
        meeting_id = request.get('id')
        is_sync = self._service.update_model(meeting_id, **request.all())
        if is_sync:
            self._set_response(MeetingSynchronizedSuccessResponse())
        else:
            self._set_response(MeetingNotSynchronizedResponse())


class SynchronizeMeetingAPI(BaseAPI):
    def _create_resource(self) -> Resource:
        return MeetingSynchronizeResource()

    PATCH = {
        'request': MeetingSynchronizedRequest
    }
