from api.factory.libs.google_libs import GoogleResponse
from src.database.postgres.user import User
from .. import BaseGoogleExecutor


class GoogleGmailExecutor(BaseGoogleExecutor):
    __GOOGLE_GMAIL_URL = 'https://www.googleapis.com/gmail/v1'

    def __init__(self, user: User):
        super().__init__()
        self._user = user

    def execute(self, *args, **kwargs) -> GoogleResponse:
        pass

    def _create_content(self, related_information: dict) -> dict:
        pass
