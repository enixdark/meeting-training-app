from src.api.pool.resources.entities.responses.implement_responses.method_responses.update_responses import \
    ResourceUpdateResponse, ListUpdatePartialResponse, ListUpdateFailedResponse, ListUpdateSuccessResponse
from src.api.pool.resources.entities.responses.response_factories.list_response_factories.list_patch_response_factories import \
    ListPatchResponseFactory


class FormResourcePatchResponseFactory(ListPatchResponseFactory):
    def _create_success_response(self, success: int, **kwargs) -> ResourceUpdateResponse:
        return ListUpdateSuccessResponse(success)

    def _create_failed_response(self, failed: int, **kwargs) -> ResourceUpdateResponse:
        return ListUpdateFailedResponse(failed)

    def _create_partial_response(self, success: int, failed: int, *args, **kwargs) -> ResourceUpdateResponse:
        return ListUpdatePartialResponse(success=success, failed=failed)
