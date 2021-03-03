from datetime import datetime, timedelta

from sqlalchemy import true

from src.api.pool.services.meeting_services.meeting_time_services import MeetingTimeService, Meeting


class MeetingLocationService(MeetingTimeService):
    def get_location_meetings(self, location_id: int, from_date: datetime, to_date: datetime):
        query = self.session.query(Meeting) \
            .filter(Meeting.state == true(),
                    Meeting.location_id == location_id,
                    Meeting.started_time >= from_date,
                    Meeting.finished_time <= to_date + timedelta(days=1))

        return query.all()
