from datetime import datetime

from . import MeetingExaminator


class TimeExaminator(MeetingExaminator):
    def state_message(self, old_stated_time: datetime, new_stated_time: datetime, ) -> str:
        time_comparision = self.__compare_time(old_stated_time, new_stated_time)
        if time_comparision > 0:
            tmp_str = '- Thời gian sang lúc {time}, ngày {date},'.format(
                time=new_stated_time.strftime('%H:%M:%S'),
                date=new_stated_time.strftime('%m/%d/%Y'))
            if time_comparision == 1:
                tmp_str += ' sớm hơn so với lịch cũ.'
            else:
                tmp_str += ' muộn hơn so với lịch cũ.'
            return tmp_str
        return ''

    @staticmethod
    def __compare_time(old_time: datetime, new_time: datetime) -> int:
        if old_time > new_time:
            return 1
        elif old_time < new_time:
            return 2
        else:
            return 0
