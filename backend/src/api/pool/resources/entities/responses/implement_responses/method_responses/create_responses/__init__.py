from src.api.pool.resources.entities.responses import MultiResourceResponse


class ResourceCreateResponse(MultiResourceResponse):
    pass


class ListCreatePartialResponse(ResourceCreateResponse):
    def __init__(self, success: int, failed: int):
        super().__init__(success, failed)
        self.response_message = 'List created partially'
        self.response_code = 207


class ListCreateSuccessResponse(ListCreatePartialResponse):
    def __init__(self, success: int):
        super().__init__(success=success, failed=0)
        self.response_code = 201
        self.response_message = 'List create successfully'


class ListCreateErrorResponse(ListCreatePartialResponse):
    def __init__(self, failed: int):
        super().__init__(success=0, failed=failed)
        self.response_message = 'List create failed'
        self.response_code = 400


class SingleCreateSuccessResponse(ListCreateSuccessResponse):
    def __init__(self):
        super().__init__(1)
        self.response_message = 'Create successfully'


class SingleCreateErrorResponse(ListCreateErrorResponse):
    def __init__(self):
        super().__init__(1)
        self.response_message = 'Create failed'
