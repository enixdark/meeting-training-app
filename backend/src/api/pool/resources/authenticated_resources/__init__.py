from src.api.pool.decorators.auth_decorator import AuthenticatedDecorator
from .. import Request


class AuthenticatedResourceHelper:
    @staticmethod
    def set_authenticated_user(request: Request,
                               auth_service: AuthenticatedDecorator) -> AuthenticatedDecorator:
        authentication = request.get_authentication()
        auth_service.set_authenticated_user(auth_user_id=authentication['id'])
        return auth_service
