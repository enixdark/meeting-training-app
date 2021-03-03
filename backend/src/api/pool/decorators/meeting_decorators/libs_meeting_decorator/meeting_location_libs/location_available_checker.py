from datetime import datetime

from src.database.postgres.meeting import Meeting
from . import MeetingLocation


class LocationAvailableChecker(MeetingLocation):
    def execute(self, location_meetings: list, meeting_started_datetime: datetime,
                meeting_finished_datetime: datetime, *args, **kwargs) -> bool:
        """
        Check if meeting started time and finished time overlay location's available meetings.
        :param location_meetings: List of available location meetings.
        :param meeting_started_datetime: datetime, meeting stated_time.
        :param meeting_finished_datetime: datetime, meeting finished_time.
        :param args:
        :param kwargs:
        :return: True if meeting is not overlays location's available meetings.
        """
        if not isinstance(location_meetings, list):
            return False
        for location_meeting in location_meetings:
            if isinstance(location_meeting, Meeting):
                location_meeting_started_datetime = location_meeting.started_time
                location_meeting_finished_datetime = location_meeting.finished_time

                # False if available meeting duration time is in new meeting times duration time
                if location_meeting_started_datetime >= meeting_started_datetime:
                    if location_meeting_started_datetime < meeting_finished_datetime:
                        return False
                # False if new meeting duration time is in available meeting duration time
                elif location_meeting_started_datetime < meeting_started_datetime:
                    if location_meeting_finished_datetime >= meeting_finished_datetime:
                        return False
        return True
