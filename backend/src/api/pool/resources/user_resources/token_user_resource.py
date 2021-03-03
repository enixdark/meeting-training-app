from src.api.pool.decorators.user_decorators.login_decorators.token_login_decorator import TokenLoginDecorator
from .. import BaseAPI, Resource, Service, authenticate, Request
from ..entities.requests.implement_requests.user_requests import TokenLoginRequest
from ..entities.responses.login_responses import LoginSuccessResponse, LoginErrorResponse


class TokenUserResource(Resource):
    def _create_service(self) -> Service:
        return TokenLoginDecorator()

    @staticmethod
    def handle_identity(request: Request) -> dict:
        return {'user': True}

    '''
        data dictionary includes:
            request: request information
            authorization: user information that is decoded in jwt    
    '''

    def post(self, request: Request, *args, **kwargs):
        user = self._service.find_model(pairs={}, **request.all())
        authentication = authenticate(user)
        if authentication:
            self._set_response(LoginSuccessResponse())
            return {
                'jwt': authentication,
                'user': user.serialize(inclusion_rs=['roles'])
            }
        self._set_response(LoginErrorResponse())


class TokenUserAPI(BaseAPI):
    def _create_resource(self) -> Resource:
        return TokenUserResource()

    POST = {
        'request': TokenLoginRequest
    }
