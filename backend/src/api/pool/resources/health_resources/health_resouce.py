from src.api.pool.services.user_services import UserFormService
from src.message_queue.tasks.cell_task import CellTask
from .. import Resource, BaseAPI, Service, Request
from ..entities.requests.implement_requests.health_request import HealthGetRequest
from ..entities.responses.health_response import HealthResponse


class HealthResource(Resource):
    def _create_service(self) -> Service:
        return UserFormService()

    @staticmethod
    def handle_identity(request_type: type(Request)) -> dict:
        return {'user': True}

    def get(self, request: Request, *args, **kwargs):
        CellTask().delay()
        self._set_response(HealthResponse())


class HealthAPI(BaseAPI):
    def _create_resource(self) -> Resource:
        return HealthResource()

    GET = {
        'request': HealthGetRequest
    }
