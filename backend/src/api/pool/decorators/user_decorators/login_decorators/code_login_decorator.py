from src.api.factory.libs.google_libs import GoogleAuthenticateExecutor
from src.api.pool.decorators.user_decorators import UserDecorator, Service
from src.api.pool.decorators.user_decorators.login_decorators.token_login_decorator import TokenLoginDecorator
from src.database.postgres.base import Model


class CodeLoginDecorator(UserDecorator):
    def _create_service(self) -> Service:
        return TokenLoginDecorator()

    def find_model(self, pairs: dict, **kwargs) -> Model:
        authentication_service = GoogleAuthenticateExecutor()
        google_response = authentication_service.execute(**kwargs)
        if google_response.status:
            return super().find_model(pairs={}, **google_response.data)
