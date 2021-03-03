from src.api.pool.resources.entities.responses import ResourceResponse


class HealthResponse(ResourceResponse):
    def __init__(self):
        super().__init__()
        self.response_code = 200
        self.response_message = "I'm alive"
