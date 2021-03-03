from abc import ABC, abstractmethod


class MeetingTimeBlock(ABC):
    @abstractmethod
    def get_time_block(self, *args, **kwargs) -> list:
        """
        Create a list of time block, like:
        [
            {
                "start" : 09:00:00,
                "finish" : 09:30:00
            },
            {
                "start" : 10:00:00,
                "finish" : 10:30:00
            },
            ...
        ]
        :param args:
        :param kwargs:
        :return:
        """
        pass
