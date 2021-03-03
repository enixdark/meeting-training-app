from src.api.pool.resources import Resource, Service, BaseAPI, Request
from src.api.pool.resources.entities.requests.implement_requests.meeting_requests.meeting_search_request import \
    MeetingSearchRequest
from src.api.pool.resources.entities.responses.implement_responses.method_responses.get_responses.meeting_search_response import \
    MeetingSearchResponse
from src.api.pool.services.meeting_services.meeting_time_services.meeting_name_services import MeetingNameService


class MeetingSearchResource(Resource):
    def _create_service(self) -> Service:
        return MeetingNameService()

    def get(self, request: Request, *args, **kwargs):
        if isinstance(self._service, MeetingNameService):
            similar = request.get('q')
            total = self._service.count_meetings_by_name(similar_name=similar, **request.all())
            self._set_response(MeetingSearchResponse(total))
            return [meeting.serialize(inclusion_rs=request.get('relations')) for meeting in
                    self._service.get_meetings_by_name(similar, **request.all())]


class MeetingSearchAPI(BaseAPI):
    def _create_resource(self) -> Resource:
        return MeetingSearchResource()

    GET = {
        'request': MeetingSearchRequest
    }
