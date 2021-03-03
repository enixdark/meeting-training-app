from sqlalchemy import false

from src.api.pool.services.meeting_services import Meeting
from src.api.pool.services.meeting_services.periodic_meeting_services import PeriodicMeetingFormService


class PeriodicInactiveFormService(PeriodicMeetingFormService):
    def get_available_periodic_meetings(self, periodic_id: str):
        query = self.session.query(Meeting) \
            .filter(
            Meeting.started_time > self._NOW,
            Meeting.periodic_id == periodic_id,
            Meeting.state == false(),
            Meeting.is_approval == false())
        return query.all()
