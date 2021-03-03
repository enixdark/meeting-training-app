from abc import ABC

from src.database.postgres.meeting import Meeting
from . import MeetingTimeBlock


class BaseOccupiedTimeBlock(MeetingTimeBlock, ABC):
    def _create_occupied_blocks(self, location_meetings: list, include_meeting=False) -> list:
        try:
            if include_meeting:
                return self.__create_occupied_blocks_with_meetings(location_meetings)
            return self.__create_occupied_blocks_without_meetings(location_meetings)
        except ValueError:
            return []

    def __create_occupied_blocks_with_meetings(self, location_meetings: list):
        """
        Create a list time block with meeting, like:
        [
            {
                "start" : 09:00:00,
                "finish" : 09:30:00
                "meeting" : {'meeting data here'}
            },
            {
                "start" : 10:00:00,
                "finish" : 10:30:00
                "meeting" : {'meeting data here'}
            }
            {
                "start" : 10:00:00,
                "finish" : 10:30:00
                "meeting" : {'meeting data here'}
            },
            ...
        ]
        :param location_meetings:
        :return: a list likes above
        """
        location_meeting_time_blocks = []
        for location_meeting in location_meetings:
            location_meeting_time_block = self.__create_occupied_block(location_meeting)
            location_meeting_time_blocks.append(self.__add_meeting(location_meeting, location_meeting_time_block))
        return location_meeting_time_blocks

    def __create_occupied_blocks_without_meetings(self, location_meetings: list):
        """
        Create a list time block without meeting, like:
        [
            {
                "start" : 09:00:00,
                "finish" : 09:30:00
            },
            {
                "start" : 10:00:00,
                "finish" : 10:30:00
            }
            {
                "start" : 10:00:00,
                "finish" : 10:30:00
            },
            ...
        ]
        :param location_meetings:
        :return: a list likes above
        """
        location_meeting_time_blocks = []
        for location_meeting in location_meetings:
            location_meeting_time_block = self.__create_occupied_block(location_meeting)
            location_meeting_time_blocks.append(location_meeting_time_block)
        return location_meeting_time_blocks

    @staticmethod
    def __create_occupied_block(location_meeting: Meeting) -> dict:
        """
        Create an item that was occupied by a meeting in time block list
        :param location_meeting:
        :return:
        """
        location_meeting_time_block = {}
        location_meeting_started_datetime = location_meeting.started_time
        location_meeting_finished_datetime = location_meeting.finished_time

        location_meeting_time_block['start'] = location_meeting_started_datetime.time()
        location_meeting_time_block['finish'] = location_meeting_finished_datetime.time()
        return location_meeting_time_block

    @staticmethod
    def __add_meeting(location_meeting: Meeting, location_meeting_time_block: dict) -> dict:
        """
        Create an item that was occupied by a meeting in time block list, with meeting
        :param location_meeting:
        :param location_meeting_time_block: add meeting to this block
        :return:
        """
        location_meeting_time_block['meeting'] = location_meeting.serialize(exclusion=['started_time', 'finished_time'])
        return location_meeting_time_block


class OccupiedTimeBlock(BaseOccupiedTimeBlock):
    def get_time_block(self, location_meetings: list, *args, **kwargs) -> list:
        return self._create_occupied_blocks(location_meetings)


class OccupiedModuleTimeBlock(BaseOccupiedTimeBlock):
    def get_time_block(self, location_meetings: list, *args, **kwargs) -> list:
        return self._create_occupied_blocks(location_meetings, True)
