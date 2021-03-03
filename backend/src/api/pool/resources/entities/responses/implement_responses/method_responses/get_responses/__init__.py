from src.api.pool.resources.entities.responses import ResourceResponse


class ResourceGetResponse(ResourceResponse):
    def __init__(self):
        super().__init__()

    def serialize(self) -> dict:
        return {
            **super().serialize(),
            'data': self.response_data
        }


class ResourceGetSuccessResponse(ResourceGetResponse):
    def __init__(self):
        super().__init__()
        self.response_message = 'Data found.'
        self.response_code = 200


class ResourceNotFoundResponse(ResourceGetResponse):
    def __init__(self):
        super().__init__()
        self.response_message = 'Data not found.'
        self.response_code = 404


class ResourceListSuccessResponse(ResourceGetSuccessResponse):
    def __init__(self):
        super().__init__()
        self.response_data = []

    def serialize(self) -> dict:
        return {
            **super().serialize(),
            'count': len(self.response_data)
        }
