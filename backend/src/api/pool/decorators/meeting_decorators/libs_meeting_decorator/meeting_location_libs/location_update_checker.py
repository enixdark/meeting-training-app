from datetime import datetime

from . import MeetingLocation
from .location_available_checker import LocationAvailableChecker


class LocationUpdateChecker(MeetingLocation):
    def __init__(self):
        self.__checker = LocationAvailableChecker()

    def execute(self, meeting_id, location_meetings: list,
                meeting_started_datetime: datetime, meeting_finished_datetime: datetime,
                *args, **kwargs) -> bool:
        """
        For update meeting, remove updated meeting from location_meetings list to compare
        """
        index = 0
        for location_meeting in location_meetings:
            if location_meeting.id == meeting_id:
                location_meetings.pop(index)
                break
            index += 1
        return self.__checker.execute(location_meetings, meeting_started_datetime, meeting_finished_datetime)
