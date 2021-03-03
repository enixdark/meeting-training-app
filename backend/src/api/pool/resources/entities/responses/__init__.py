class ResourceResponse:
    def __init__(self):
        self.response_message = ''
        self.response_code = None
        self.response_data = {}

    """
        Override serialize function to custom response key
    """

    def serialize(self) -> dict:
        return {
            'code': self.response_code,
            'message': self.response_message
        }


class MultiResourceResponse(ResourceResponse):
    def __init__(self, success: int, failed: int):
        super().__init__()
        self.success = success
        self.failed = failed
        self.response_data = []

    def serialize(self) -> dict:
        return {
            **super().serialize(),
            'data': self.response_data,
            'success': self.success,
            'failed': self.failed
        }
