from src.api.pool.decorators.user_decorators.login_decorators.code_login_decorator import CodeLoginDecorator
from src.api.pool.resources.user_resources.token_user_resource import TokenUserResource
from .. import BaseAPI, Resource, Service
from ..entities.requests.implement_requests.user_requests import CodeLoginRequest


class CodeUserResource(TokenUserResource):
    def _create_service(self) -> Service:
        return CodeLoginDecorator()
    '''
        data dictionary includes:
            request: request information
            authorization: user information that is decoded in jwt    
    '''


class CodeUserAPI(BaseAPI):
    def _create_resource(self) -> Resource:
        return CodeUserResource()

    POST = {
        'request': CodeLoginRequest
    }
