from datetime import datetime

from src.database.postgres.location import Location
from . import MeetingLocation


class LocationBoundaryChecker(MeetingLocation):
    def execute(self, location,
                meeting_started_datetime: datetime, meeting_finished_datetime: datetime,
                *args, **kwargs) -> bool:
        """
        Check if meeting started time and finished time overlay location opened and closed time
        :param location:
        :param meeting_started_datetime:
        :param meeting_finished_datetime:
        :param args:
        :param kwargs:
        :return:
        """
        if isinstance(location, Location):
            location_opened_time = location.opened_time
            location_closed_time = location.closed_time
            meeting_started_time = meeting_started_datetime.time()
            meeting_finished_time = meeting_finished_datetime.time()
            # check meeting time with location time
            if meeting_started_time >= location_opened_time and meeting_finished_time <= location_closed_time:
                return True
            return False
