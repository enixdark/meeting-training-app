from . import UserGetRequest, GetSchema
from .user_schemas.user_sugest_schema import UserSuggestSchema


class UserSuggestRequest(UserGetRequest):
    def _create_schema(self) -> GetSchema:
        return UserSuggestSchema()

    def filter_rules(self) -> dict:
        return {
            **super().filter_rules(),
            'q': self._get_email_query()
        }

    def _get_email_query(self):
        return self._get_url_parameter('q')
