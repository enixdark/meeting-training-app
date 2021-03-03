from marshmallow import ValidationError, validates_schema, fields

from src.api.pool.resources.entities.requests.implement_requests.user_requests.user_schemas import UserSchema
from ..meeting_user_schema import MeetingUserSchema
from ....base_requests.schemas.common_schemas.common_datetimes.common_started_datetime import CommonStartedDatetime, \
    CommonDatetime
from ....base_requests.schemas.common_schemas.common_strings.extra_long_string import ExtraLongString
from ....base_requests.schemas.common_schemas.common_strings.normal_string import NormalString
from ....base_requests.schemas.common_schemas.common_unsigned_integer.unsigned_integer import UnsignedInteger
from ....base_requests.schemas.get_schema import GetSchema
from ....base_requests.schemas.post_schema import PostSchema


class MeetingSchema(PostSchema):
    name = NormalString()
    description = ExtraLongString()
    location_id = UnsignedInteger()
    started_time = CommonStartedDatetime()
    finished_time = CommonDatetime()


class MeetingPostSchema(MeetingSchema):
    creator_id = UnsignedInteger()
    attendees = fields.List(fields.Nested(UserSchema))

    @staticmethod
    def _create_required_attributes() -> list:
        return ['name', 'description', 'location_id', 'creator_id', 'started_time', 'finished_time']

    @validates_schema
    def validate_time_order(self, data, **kwargs):
        errors = {}
        started_time = data.get('started_time', None)
        finished_time = data.get('finished_time', None)
        if started_time and finished_time:
            if started_time >= finished_time:
                errors['time_order'] = 'started_time be greater than finished_time.'
            if started_time.date() != finished_time.date():
                errors['date_order'] = 'started_time and finished_time must have the same date.'
            if errors:
                raise ValidationError(errors)


class MeetingPatchSchema(MeetingSchema):
    id = UnsignedInteger()
    attendees = fields.List(fields.Nested(MeetingUserSchema))

    @staticmethod
    def _create_required_attributes() -> list:
        return ['id']

    @validates_schema
    def validate_time_order(self, data, **kwargs):
        errors = {}
        if data:
            started_time = data.get('started_time', None)
            finished_time = data.get('finished_time', None)

            if started_time and not finished_time:
                errors['finished_time'] = 'started_time and finished_time must be both included.'
            elif not started_time and finished_time:
                errors['started_time'] = 'started_time and finished_time must be both included.'
            elif started_time and finished_time:
                if started_time >= finished_time:
                    errors['time_order'] = 'started_time be greater than finished_time.'
                if started_time.date() != finished_time.date():
                    errors['date_order'] = 'started_time and finished_time must have the same date.'
        if errors:
            raise ValidationError(errors)


class MeetingGetSchema(GetSchema):
    @staticmethod
    def sort_rule() -> list:
        return ['id']

    @staticmethod
    def relation_rule() -> list:
        return ['location', 'creator', 'attendees']


class MeetingDeleteSchema(MeetingSchema):
    id = UnsignedInteger()

    @staticmethod
    def _create_required_attributes() -> list:
        return ['id']
