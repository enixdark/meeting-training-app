from src.api.pool.resources.entities.requests.base_requests.schemas.common_schemas.common_datetimes import \
    CommonDatetime
from . import MeetingPostSchema


class MeetingPeriodicPostSchema(MeetingPostSchema):
    started_time = CommonDatetime()
