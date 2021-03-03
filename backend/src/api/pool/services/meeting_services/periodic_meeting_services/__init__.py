from sqlalchemy import true

from src.api.pool.services.meeting_services.meeting_time_services import MeetingTimeService, Meeting


class PeriodicMeetingFormService(MeetingTimeService):
    def get_available_periodic_meetings(self, periodic_id: str):
        query = self.session.query(Meeting) \
            .filter(
            Meeting.started_time > self._NOW,
            Meeting.periodic_id == periodic_id,
            Meeting.state == true())
        return query.all()

    def get_all_periodic_meetings(self, periodic_id: str):
        query = self.session.query(Meeting) \
            .filter(
            Meeting.periodic_id == periodic_id,
        )
        return query.all()
