from src.api.pool.resources.entities.responses import MultiResourceResponse


class ResourceUpdateResponse(MultiResourceResponse):
    pass


class ListUpdatePartialResponse(ResourceUpdateResponse):
    def __init__(self, success: int, failed: int):
        super().__init__(success, failed)
        self.response_message = 'Partial list updated successfully.'
        self.response_code = 207


class ListUpdateSuccessResponse(ListUpdatePartialResponse):
    def __init__(self, success: int):
        super().__init__(success=success, failed=0)
        self.response_message = 'List update successfully.'
        self.response_code = 200


class ListUpdateFailedResponse(ListUpdatePartialResponse):
    def __init__(self, failed: int):
        super().__init__(success=0, failed=failed)
        self.response_message = 'List update failed.'
        self.response_code = 400


class SingleUpdateSuccessResponse(ListUpdateSuccessResponse):
    def __init__(self):
        super().__init__(1)
        self.response_message = 'Update successfully.'


class SingleUpdateFailedResponse(ListUpdateFailedResponse):
    def __init__(self):
        super().__init__(1)
        self.response_message = 'Update failed.'
