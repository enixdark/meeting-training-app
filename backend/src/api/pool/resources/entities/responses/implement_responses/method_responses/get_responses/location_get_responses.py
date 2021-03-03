from . import ResourceGetResponse, ResourceListSuccessResponse


class LocationResourceGetResponse(ResourceGetResponse):
    def __init__(self):
        super().__init__()
        self.response_message = 'Location found.'

    def serialize(self) -> dict:
        return {
            **super().serialize(),
            'count': 1
        }


class LocationListResourceResponse(ResourceListSuccessResponse):
    def __init__(self):
        super().__init__()
        self.response_message = 'Location list found.'


class LocationListErrorResourceResponse(ResourceListSuccessResponse):
    def __init__(self):
        super().__init__()
        self.response_code = 404
        self.response_message = 'Location len is 0.'
