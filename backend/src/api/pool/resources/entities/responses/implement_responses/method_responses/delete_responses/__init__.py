from src.api.pool.resources.entities.responses import MultiResourceResponse


class ResourceDeleteResponse(MultiResourceResponse):
    pass


class ListDeletePartialResponse(ResourceDeleteResponse):
    def __init__(self, success: int, failed: int):
        super(ListDeletePartialResponse, self).__init__(success, failed)
        self.response_message = 'List delete partial successfully'
        self.response_code = 207


class ListDeleteSuccessResponse(ListDeletePartialResponse):
    def __init__(self, success: int):
        super(ListDeleteSuccessResponse, self).__init__(success=success, failed=0)
        self.response_message = 'List delete successfully'
        self.response_code = 200


class ListDeleteFailedResponse(ListDeletePartialResponse):
    def __init__(self, failed: int):
        super(ListDeleteFailedResponse, self).__init__(success=0, failed=failed)
        self.response_message = 'List delete failed'
        self.response_code = 400


class SingleDeleteSuccessResponse(ListDeleteSuccessResponse):
    def __init__(self):
        super().__init__(success=1)
        self.response_message = 'Delete successfully'


class SingleDeleteFailedResponse(ListDeleteFailedResponse):
    def __init__(self):
        super().__init__(failed=1)
        self.response_message = 'Delete failed.'
