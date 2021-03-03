from abc import ABC
from datetime import datetime, time, timedelta

from config import BaseApiConfig
from . import MeetingTimeBlock


class BaseAvailableTimeBlock(MeetingTimeBlock, ABC):
    def _create_available_blocks(self, meeting_time_blocks, date: datetime.date,
                                 location_opened_time, location_closed_time, include_meeting=False) -> list:
        try:
            if include_meeting:
                return self.__create_available_blocks_with_occupied(meeting_time_blocks,
                                                                    location_opened_time, location_closed_time)
            return self.__create_available_blocks_without_occupied(meeting_time_blocks, date,
                                                                   location_opened_time, location_closed_time)
        except KeyError:
            return []

    def __create_available_blocks_without_occupied(self, meeting_time_blocks, date: datetime.date,
                                                   location_opened_time, location_closed_time) -> list:
        """
        Based on meeting_time block, create a available time block without meeting_time_block, like:
        [
            {
                "start" : 09:00:00,
                "finish" : 09:30:00
            },
            ///a time block that is occupied by a meeting is not included
            {
                "start" : 10:00:00,
                "finish" : 10:30:00
            }
            ...
        ]
        :param meeting_time_blocks:
        :param date:
        :param location_opened_time:
        :param location_closed_time:
        :return:
        """
        time_blocks = []
        pivot = self.__create_current_pivot()
        if date == datetime.now().date():
            if location_opened_time > pivot:
                previous = location_opened_time
            else:
                previous = pivot
        else:
            previous = location_opened_time
        for occupied in meeting_time_blocks:
            if occupied['start'] > previous:
                available_block = self.__create_available_block(previous, occupied['start'])
                time_blocks.append(available_block)
            if occupied['finish'] > previous:
                previous = occupied['finish']
        else:
            if previous < location_closed_time:
                available_block = self.__create_available_block(previous, location_closed_time)
                time_blocks.append(available_block)

        return time_blocks

    def __create_available_blocks_with_occupied(self, meeting_time_blocks,
                                                location_opened_time, location_closed_time) -> list:
        """
        Based on meeting_time block, create a available time block with meeting_time_block, like:
        [
            {
                "start" : 09:00:00,
                "finish" : 09:30:00
            },
            {
                "start" : 09:30:00,
                "finish" : 10:00:00,
                "meeting": {meeting data here}
            }
            {
                "start" : 10:00:00,
                "finish" : 10:30:00
            },
            ...
        ]
        :param meeting_time_blocks:
        :param location_opened_time:
        :param location_closed_time:
        :return:
        """
        time_blocks = []
        previous = location_opened_time
        for occupied in meeting_time_blocks:
            if occupied['start'] > previous:
                available_block = self.__create_available_block(previous, occupied['start'])
                time_blocks.append(available_block)
                occupied_block = self.__create_occupied_block(occupied)
                time_blocks.append(occupied_block)
            else:
                occupied_block = self.__create_occupied_block(occupied)
                time_blocks.append(occupied_block)
            previous = occupied['finish']
        else:
            if previous < location_closed_time:
                available_block = self.__create_available_block(previous, location_closed_time)
                time_blocks.append(available_block)

        return time_blocks

    @staticmethod
    def __create_available_block(start: datetime, finished: datetime) -> dict:
        available_block = dict()
        available_block['start'] = start.isoformat()
        available_block['finish'] = finished.isoformat()
        return available_block

    @staticmethod
    def __create_occupied_block(occupied: dict) -> dict:
        occupied_block = dict()
        occupied_block['meeting'] = occupied['meeting']
        occupied_block['start'] = occupied['start'].isoformat()
        occupied_block['finish'] = occupied['finish'].isoformat()
        return occupied_block

    @staticmethod
    def __create_current_pivot():
        """
        Ceil current time to the next 30 or 00 minutes
        :return:
        """
        now = datetime.now() + timedelta(hours=int(BaseApiConfig.TIME_DIFFERENCE))
        now = now.time()
        hour = now.hour

        minute = now.minute
        if minute <= 30:
            minute = 30
        else:
            tmp_time = datetime.now() + timedelta(hours=1 + int(BaseApiConfig.TIME_DIFFERENCE))
            hour = tmp_time.hour
            minute = 0
        return time(hour, minute, 0)


class AvailableTimeBlock(BaseAvailableTimeBlock):
    def get_time_block(self, meeting_time_blocks, date: datetime.date, location_opened_time, location_closed_time,
                       *args, **kwargs) -> list:
        return self._create_available_blocks(meeting_time_blocks, date, location_opened_time, location_closed_time)


class AvailableModuleTimeBlock(BaseAvailableTimeBlock):
    def get_time_block(self, meeting_time_blocks, date: datetime.date, location_opened_time, location_closed_time,
                       *args, **kwargs) -> list:
        return self._create_available_blocks(meeting_time_blocks, date, location_opened_time, location_closed_time,
                                             True)
