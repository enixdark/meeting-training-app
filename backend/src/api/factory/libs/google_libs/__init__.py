import json
from abc import ABC, abstractmethod

import requests

from config import BaseApiConfig
from src.api.factory.exceptions.service_exceptions.connection_exception import ConnectionException
from src.api.factory.exceptions.service_exceptions.google_exceptions import InvalidAuthenticationCodeException


class GoogleResponse(ABC):
    def __init__(self):
        # data acquired from google
        self.data = {}
        # status of the execute method
        self.status = False


class GoogleExecutor(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs) -> GoogleResponse:
        pass

    @abstractmethod
    def refresh_access_token(self, refresh_token) -> str:
        pass


class BaseGoogleExecutor(GoogleExecutor, ABC):
    def __init__(self):
        self.__response = GoogleResponse()

    def _create_response(self, data: dict, status=True) -> GoogleResponse:
        self.__response.data = data
        self.__response.status = status
        return self.__response

    def refresh_access_token(self, refresh_token) -> str:
        """
        Refresh google api access token.
        """
        data = {
            'refresh_token': refresh_token,
            'client_id': BaseApiConfig.CLIENT_ID,
            'client_secret': BaseApiConfig.CLIENT_SECRET,
            'grant_type': 'refresh_token'
        }
        google_token_url = 'https://www.googleapis.com/oauth2/v4/token'
        response = self._request(method='post', url=google_token_url, **{'data': data})
        if response:
            response_content = json.loads(response.content.decode())
            return response_content['access_token']
        return ''

    @staticmethod
    def _request(method: str, url: str, **kwargs):
        """
        Request with ConnectionError handler
        """
        try:
            response = requests.request(method, url, **kwargs)
            if response.status_code == 200:
                return response
            return None
        except ConnectionError:
            raise ConnectionException()


class GoogleAuthenticateExecutor(BaseGoogleExecutor):
    """
    Get access token with google authorization code
    """

    def execute(self, *args, **kwargs) -> GoogleResponse:
        code = kwargs.get('code', None)
        if code:
            data = {'code': code,
                    'redirect_uri': BaseApiConfig.REDIRECT_URI,
                    'client_id': BaseApiConfig.CLIENT_ID,
                    'client_secret': BaseApiConfig.CLIENT_SECRET,
                    'grant_type': 'authorization_code'}
            response = self._request(method='post', url='https://www.googleapis.com/oauth2/v4/token', **{'data': data})
            if response:
                response_content = json.loads(response.content.decode())
                access_token = response_content.get('access_token', None)
                if access_token:
                    return self._create_response(response_content)
                raise InvalidAuthenticationCodeException()
        return self._create_response({}, False)
