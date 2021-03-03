from abc import ABC

from marshmallow import ValidationError

from src.api.factory.exceptions import ApplicationException
from src.api.pool.resources.entities.responses import ResourceResponse


class ExceptionResourceResponse(ResourceResponse, ABC):
    def serialize(self) -> dict:
        return {
            **super().serialize(),
            'data': {}
        }


class ApplicationExceptionResourceResponse(ExceptionResourceResponse, ABC):
    def __init__(self, exception: ApplicationException):
        super().__init__()
        self.response_code = exception.get_response_code()
        self.response_message = exception.get_message()


class ValidationExceptionResourceResponse(ExceptionResourceResponse):
    __BAD_PARAMS_RESPONSE_CODE = 400

    def __init__(self, exception: ValidationError):
        super().__init__()
        self.response_code = self.__BAD_PARAMS_RESPONSE_CODE
        self.response_message = eval(str(exception))
