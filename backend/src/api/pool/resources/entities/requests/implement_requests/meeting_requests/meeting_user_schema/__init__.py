from marshmallow import fields

from ....base_requests.schemas.common_schemas.common_emails.allowed_email import \
    AllowedDomainEmail
from ....base_requests.schemas.post_schema import PostSchema


class MeetingUserSchema(PostSchema):
    email = AllowedDomainEmail(required=True)
    is_accepted = fields.Boolean(required=True)
    may_join = fields.Boolean(required=True)
