from src.api.pool.resources.entities.responses.implement_responses.method_responses.delete_responses import \
    ResourceDeleteResponse, ListDeleteSuccessResponse, ListDeleteFailedResponse, ListDeletePartialResponse
from . import ListDeleteResponseFactories


class FormResourceDeleteResponseFactory(ListDeleteResponseFactories):
    def _create_success_response(self, success: int, **kwargs) -> ResourceDeleteResponse:
        return ListDeleteSuccessResponse(success)

    def _create_failed_response(self, failed: int, **kwargs) -> ResourceDeleteResponse:
        return ListDeleteFailedResponse(failed)

    def _create_partial_response(self, success: int, failed: int, **kwargs) -> ResourceDeleteResponse:
        return ListDeletePartialResponse(success=success, failed=failed)