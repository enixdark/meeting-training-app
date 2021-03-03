from src.api.pool.resources.entities.responses.implement_responses.method_responses.get_responses import \
    ResourceListSuccessResponse


class MeetingSearchResponse(ResourceListSuccessResponse):
    def __init__(self, total: int):
        super(MeetingSearchResponse, self).__init__()
        self.total = total

    def serialize(self) -> dict:
        return {
            **super().serialize(),
            'total': self.total
        }
