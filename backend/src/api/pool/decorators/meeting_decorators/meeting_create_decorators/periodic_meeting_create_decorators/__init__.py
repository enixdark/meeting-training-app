from abc import ABC, abstractmethod
from datetime import datetime

from .. import BaseCreateMeetingDecorator, Model
from ... import Service, MeetingAuthDecorator


class BaseMeetingPeriodicCreateDecorator(MeetingAuthDecorator, ABC):
    def __init__(self):
        super(BaseMeetingPeriodicCreateDecorator, self).__init__()
        self.__periodic_id = self.__create_periodic_id()

    def _create_service(self) -> Service:
        return BaseCreateMeetingDecorator()

    def create_new_model(self, *args, **kwargs) -> Model:
        """
        Create periodic meeting. (Same with create meeting, just add an extra step by adding periodic_id to kwargs)
        :param args: create meeting list data
        :param kwargs: create meeting dict data
        :return: New periodic meeting
        """
        kwargs['periodic_id'] = self.__periodic_id
        kwargs['is_periodic'] = True
        kwargs = self._add_periodic_state(**kwargs)
        return super(BaseMeetingPeriodicCreateDecorator, self).create_new_model(*args, **kwargs)

    @abstractmethod
    def _add_periodic_state(self, **kwargs) -> dict:
        pass

    @staticmethod
    def __create_periodic_id() -> str:
        """
        Create periodic id for periodic meeting. Base on time
        :return: An unique id base on time (day-month-year-hour-minute-second-millisecond), like: 09192019161312808472
        """
        now = datetime.now()
        return now.strftime("%m%d%Y%H%M%S%f")
