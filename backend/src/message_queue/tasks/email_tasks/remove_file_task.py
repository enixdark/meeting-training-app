from datetime import datetime, timedelta

from config import BaseApiConfig
from src.message_queue.tasks import BaseMeetingTask
import os


class RemoveFileTask(BaseMeetingTask):
    __NOW = datetime.now() + timedelta(hours=BaseApiConfig.TIME_DIFFERENCE)

    def run(self, *args, **kwargs):
        from_date = kwargs.get('from_date', self.__NOW + timedelta(days=-7))
        to_date = kwargs.get('to_date', self.__NOW + timedelta(days=7))

        # celery modify date time to string ---> need to secure data type
        if isinstance(from_date, str):
            from_date = datetime.strptime(from_date, '%Y-%m-%dT%H:%M:%S')
        if isinstance(to_date, str):
            to_date = datetime.strptime(to_date, '%Y-%m-%dT%H:%M:%S')

        f_date = datetime.strftime(from_date, '%d-%m-%Y')
        t_date = datetime.strftime(to_date, '%d-%m-%Y')
        os.remove('vMeeting_{}:{}.xls'.format(f_date, t_date))
