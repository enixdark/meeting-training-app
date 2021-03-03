from . import ResourceGetResponse, ResourceListSuccessResponse


class UserResourceGetResponse(ResourceGetResponse):
    def __init__(self):
        super().__init__()
        self.response_message = 'User found.'

    def serialize(self) -> dict:
        return {
            **super().serialize(),
            'count': 1
        }


class UserSuggestResourceResponse(ResourceListSuccessResponse):
    def __init__(self):
        super().__init__()
        self.response_message = 'User suggestion found.'


class UserSuggestNoneResourceResponse(ResourceListSuccessResponse):
    def __init__(self):
        super().__init__()
        self.response_code = 404
        self.response_message = 'User suggestion len is 0.'
