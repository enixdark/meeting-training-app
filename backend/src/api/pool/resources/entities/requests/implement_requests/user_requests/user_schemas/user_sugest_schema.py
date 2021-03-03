from . import UserGetSchema
from ....base_requests.schemas.common_schemas.common_strings.short_string import ShortString


class UserSuggestSchema(UserGetSchema):
    q = ShortString(required=True)
