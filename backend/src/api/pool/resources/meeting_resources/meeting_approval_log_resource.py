from src.api.pool.decorators.meeting_decorators.meeting_check_decorators.meeting_approval_log_decorator import \
    MeetingApprovalLogDecorator
from src.api.pool.resources.entities.requests.implement_requests.meeting_requests.meeting_approval_log_request import \
    MeetingApprovalLogRequest
from src.api.pool.resources.entities.responses.implement_responses.method_responses.get_responses.meeting_get_responses import \
    MeetingApprovalLogResponse
from .. import Service, BaseAPI, Resource, Request


class CheckApprovalLogResource(Resource):
    def _create_service(self) -> Service:
        return MeetingApprovalLogDecorator()

    def get(self, request: Request, *args, **kwargs):
        self._set_response(MeetingApprovalLogResponse())
        return self._service.get_all(**request.all())


class CheckApprovalLogAPI(BaseAPI):
    def _create_resource(self) -> Resource:
        return CheckApprovalLogResource()

    GET = {
        'request': MeetingApprovalLogRequest
    }
