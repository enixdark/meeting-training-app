from src.api.pool.services.meeting_services import MeetingInstantFormService
from .. import BaseAPI, Resource
from ..entities.requests.implement_requests.meeting_requests import MeetingGetRequest
from ..form_resource import BaseFormResource, FormService


class MeetingResource(BaseFormResource):
    def _create_service(self) -> FormService:
        return MeetingInstantFormService()


class MeetingAPI(BaseAPI):
    def _create_resource(self) -> Resource:
        return MeetingResource()

    GET = {
        'request': MeetingGetRequest
    }
