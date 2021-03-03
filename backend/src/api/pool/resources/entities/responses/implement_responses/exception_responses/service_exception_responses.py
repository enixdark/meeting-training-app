from src.api.factory.exceptions.service_exceptions import ServiceException
from src.api.pool.resources.entities.responses.implement_responses.exception_responses import ApplicationExceptionResourceResponse


class ServiceExceptionResourceResponse(ApplicationExceptionResourceResponse):
    def __init__(self, exception: ServiceException):
        super().__init__(exception)
