from src.api.pool.decorators.meeting_decorators.statistic_meeting_decorator import ListMeetingDecorator
from src.api.pool.resources.entities.responses.implement_responses.method_responses.get_responses.meeting_get_responses import \
    MeetingListResourceResponse
from .. import Service, BaseAPI, Resource, Request
from ..entities.requests.implement_requests.meeting_requests.meeting_list_request import MeetingListRequest


class ListMeetingResource(Resource):
    def _create_service(self) -> Service:
        return ListMeetingDecorator()

    def get(self, request: Request, *args, **kwargs):
        self._set_response(MeetingListResourceResponse())
        return self._service.get_all(**request.all())


class ListMeetingAPI(BaseAPI):
    def _create_resource(self) -> Resource:
        return ListMeetingResource()

    GET = {
        'request': MeetingListRequest
    }
