from src.api.pool.resources.entities.responses.implement_responses.method_responses.get_responses import \
    ResourceNotFoundResponse, ResourceGetSuccessResponse, ResourceGetResponse
from src.api.pool.resources.entities.responses.response_factories.single_response_factories import SingleResponseFactory


class FormResourceGetResponseFactory(SingleResponseFactory):
    def _create_success_response(self) -> ResourceGetResponse:
        return ResourceGetSuccessResponse()

    def _create_failed_response(self) -> ResourceGetResponse:
        return ResourceNotFoundResponse()
