from src.api.pool.resources.entities.responses import ResourceResponse


class LoginResponse(ResourceResponse):
    def serialize(self) -> dict:
        return {
            **super().serialize(),
            'data': self.response_data
        }


class LoginSuccessResponse(LoginResponse):
    def __init__(self):
        super().__init__()
        self.response_message = 'Login successfully.'
        self.response_code = 200


class LoginErrorResponse(LoginResponse):
    def __init__(self):
        super().__init__()
        self.response_message = 'Login failed.'
        self.response_code = 400
