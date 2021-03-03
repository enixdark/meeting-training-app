from src.api.factory.exceptions.authorized_exceptions import UnauthorizedException
from src.api.pool.resources.entities.responses.implement_responses.exception_responses import ApplicationExceptionResourceResponse


class AuthorizationExceptionResourceResponse(ApplicationExceptionResourceResponse):
    def __init__(self, exception: UnauthorizedException):
        super().__init__(exception)
