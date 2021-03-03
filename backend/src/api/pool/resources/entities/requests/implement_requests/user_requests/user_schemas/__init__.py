from ....base_requests.schemas import BaseSchema
from ....base_requests.schemas.common_schemas.common_emails.allowed_email import AllowedDomainEmail
from ....base_requests.schemas.common_schemas.common_strings import CommonString
from ....base_requests.schemas.get_schema import GetSchema


class UserSchema(BaseSchema):
    email = AllowedDomainEmail(required=True)


class TokenLoginSchema(BaseSchema):
    access_token = CommonString(required=True)


class UserGetSchema(GetSchema):
    @staticmethod
    def sort_rule() -> list:
        return ['id']

    @staticmethod
    def relation_rule() -> list:
        return ['roles', 'host', 'attendants']


class CodeLoginSchema(BaseSchema):
    code = CommonString(required=True)
