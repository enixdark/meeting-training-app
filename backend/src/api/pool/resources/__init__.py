from abc import abstractmethod, ABC

from flask.views import MethodView
from marshmallow import ValidationError

from src.api.factory.exceptions.authorized_exceptions import UnauthorizedException
from src.api.factory.exceptions.service_exceptions import ServiceException
from src.api.pool.services import Service
from .entities.requests import Request
from .entities.responses import ResourceResponse
from src.api.pool.resources.entities.responses.implement_responses.exception_responses import \
    ValidationExceptionResourceResponse
from src.api.pool.resources.entities.responses.implement_responses.exception_responses.authorization_exception_response import \
    AuthorizationExceptionResourceResponse
from src.api.pool.resources.entities.responses.implement_responses.exception_responses.service_exception_responses import \
    ServiceExceptionResourceResponse
from .security import authenticate, identity


class Resource(ABC):
    def __init__(self):
        self._service = self._create_service()
        self.__response = None

    @abstractmethod
    def _create_service(self) -> Service:
        pass

    '''
    To ignore authorization, override this method and return some list with length greater than 0 
    '''

    @staticmethod
    def handle_identity(request_type: type(Request)) -> dict:
        request = request_type(authentication={})
        authorization = request.header('Authorization')
        payload = identity(authorization)
        return payload

    def __handle_logic(self, request_type: type(Request), authentication) -> dict:
        request = request_type(authentication=authentication)
        request_method = request.method().lower()
        method_to_call = getattr(self, request_method)
        return method_to_call(request)

    def handle_response(self, result, code=200) -> ResourceResponse:
        if self.__response:
            if result:
                self.__response.response_data = result
            return self.__response
        response = ResourceResponse()
        response.response_data = result
        response.response_message = ''
        response.response_code = code
        return response

    def handle(self, provider: dict) -> ResourceResponse:
        request_type = provider.get('request', None)
        result = None
        if request_type:
            try:
                authentication = self.handle_identity(request_type)
                if len(authentication) > 0:
                    result = self.__handle_logic(request_type, authentication)
            except UnauthorizedException as ue:
                self._set_response(AuthorizationExceptionResourceResponse(ue))
            except ValidationError as ve:
                self._set_response(ValidationExceptionResourceResponse(ve))
            except ServiceException as se:
                self._set_response(ServiceExceptionResourceResponse(se))
            # except Exception as e:
            #     self._set_response(ServiceExceptionResourceResponse(DummyServiceException(e)))
        return self.handle_response(result)

    '''
    data dictionary parameter includes:
        request: request information
        authorization: user information that is decoded in jwt    
    '''

    def get(self, request: Request, *args, **kwargs):
        pass

    def post(self, request: Request, *args, **kwargs):
        pass

    def patch(self, request: Request, *args, **kwargs):
        pass

    def delete(self, request: Request, *args, **kwargs):
        pass

    def _set_service(self, service: Service):
        self._service = service

    def _set_response(self, response: ResourceResponse):
        self.__response = response


class BaseAPI(MethodView):
    GET = {}
    POST = {}
    PATCH = {}
    DELETE = {}

    def __init__(self):
        self._resource = self._create_resource()

    def _create_resource(self) -> Resource:
        pass

    def get(self):
        response = self._resource.handle(self.GET)
        return response.serialize(), response.response_code

    def post(self):
        response = self._resource.handle(self.POST)
        return response.serialize(), response.response_code

    def patch(self):
        response = self._resource.handle(self.PATCH)
        return response.serialize(), response.response_code

    def delete(self):
        response = self._resource.handle(self.DELETE)
        return response.serialize(), response.response_code
