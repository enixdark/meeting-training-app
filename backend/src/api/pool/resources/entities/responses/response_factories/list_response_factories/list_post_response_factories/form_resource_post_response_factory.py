from src.api.pool.resources.entities.responses.implement_responses.method_responses.create_responses import \
    ResourceCreateResponse, ListCreateSuccessResponse, ListCreateErrorResponse, ListCreatePartialResponse
from src.api.pool.resources.entities.responses.response_factories.list_response_factories.list_post_response_factories import \
    ListPostResponseFactory


class FormResourcePostResponseFactory(ListPostResponseFactory):
    def _create_success_response(self, success: int, **kwargs) -> ResourceCreateResponse:
        return ListCreateSuccessResponse(success)

    def _create_failed_response(self, failed: int, **kwargs) -> ResourceCreateResponse:
        return ListCreateErrorResponse(failed)

    def _create_partial_response(self, success: int, failed: int, *args, **kwargs) -> ResourceCreateResponse:
        return ListCreatePartialResponse(success=success, failed=failed)
