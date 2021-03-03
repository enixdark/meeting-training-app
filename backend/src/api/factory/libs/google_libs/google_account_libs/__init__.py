import json
import re

import requests

from src.api.factory.exceptions.service_exceptions.google_exceptions.email_exceptions import InvalidEmailException
from src.api.factory.exceptions.service_exceptions.google_exceptions.scope_exceptions import MissingEmailScopeException
from src.api.factory.exceptions.service_exceptions.google_exceptions.token_exceptions import InvalidAccessTokenException
from .. import GoogleResponse, BaseGoogleExecutor


class GoogleUserService(BaseGoogleExecutor):
    __GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'

    def execute(self, *args, **kwargs) -> GoogleResponse:
        access_token = kwargs.get('access_token', None)
        if access_token:
            # requests for user information and parse it to dict type
            response = requests.get(url=self.__GOOGLE_USER_INFO_URL, params={'access_token': access_token})
            response_content = json.loads(response.content.decode())

            # check existed error to determine expired access token
            error = response_content.get('error', None)
            if error:
                raise InvalidAccessTokenException()

            # check existed email to determine valid scope
            email = response_content.get('email', None)
            if email:
                return self._create_response(response_content, True)
            raise MissingEmailScopeException()
        return self._create_response({}, False)


class GoogleCheckDomainService(BaseGoogleExecutor):
    __ALLOWED_DOMAINS = ['vccorp.vn', 'gmail.com']

    def execute(self, *args, **kwargs) -> GoogleResponse:
        email = kwargs.get('email', None)
        if email:
            domain = re.search("[^.@]*?\.\w{2,}$|[^.@]*?\.com?\.\w{2}$", email)
            if domain.group() in self.__ALLOWED_DOMAINS:
                return self._create_response({}, True)
            raise InvalidEmailException()
        return self._create_response({}, False)
