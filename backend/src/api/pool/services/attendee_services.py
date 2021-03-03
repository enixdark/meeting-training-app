from sqlalchemy import true
from sqlalchemy.orm import joinedload

from src.api.pool.services import DecoratorService, FormService
from src.database.postgres.base import Model
from src.database.postgres.meeting_user import MeetingUser


class AttendeeDecoratorService(DecoratorService):
    def _create_class_model(self):
        return MeetingUser

    def get_model(self, _id, **kwargs) -> Model:
        return self._class()


class AttendeeFormService(FormService):
    def _create_class_model(self):
        return MeetingUser

    def get_meeting_coordinator(self, meeting_id: int) -> MeetingUser:
        query = self.session.query(MeetingUser) \
            .filter(MeetingUser.is_coordinator == true(),
                    MeetingUser.meeting_id == meeting_id)
        return query.first()

    def get_meeting_user(self, meeting_id: int, user_id: int) -> MeetingUser:
        query = self.session.query(MeetingUser) \
            .filter(MeetingUser.meeting_id == meeting_id,
                    MeetingUser.user_id == user_id)
        return query.first()

    def get_user_meetings(self, user_id: int, **kwargs):
        offset_number = kwargs.get('offset', None)
        limit_number = kwargs.get('limit', 0)

        query = self.session.query(MeetingUser) \
            .options(joinedload(MeetingUser.meeting)) \
            .filter(MeetingUser.user_id == user_id)
        if offset_number:
            query = query.offset(offset_number)

        return query.limit(limit_number).all()
