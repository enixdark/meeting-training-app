from src.api.pool.decorators.meeting_decorators.meeting_check_decorators.build_daily_meeting_decorator import \
    BuildTimeBlockDecorator
from src.api.pool.decorators.meeting_decorators.meeting_check_decorators.check_available_time_decorator import \
    CheckAvailableTimeDecorator
from src.api.pool.resources.entities.responses.implement_responses.method_responses.get_responses.meeting_get_responses import \
    MeetingCheckResourceResponse
from .. import Service, BaseAPI, Resource, Request
from ..entities.requests.implement_requests.meeting_requests.meeting_check_request import MeetingCheckRequest


class CheckMeetingTimeResource(Resource):
    def _create_service(self) -> Service:
        return CheckAvailableTimeDecorator()

    def get(self, request: Request, *args, **kwargs):
        self._set_response(MeetingCheckResourceResponse())
        is_include_meeting = request.get('include_meeting')
        if is_include_meeting:
            self._set_service(BuildTimeBlockDecorator())
        return self._service.get_all(**request.all())


class CheckMeetingTimeAPI(BaseAPI):
    def _create_resource(self) -> Resource:
        return CheckMeetingTimeResource()

    GET = {
        'request': MeetingCheckRequest
    }
