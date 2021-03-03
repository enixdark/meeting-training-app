from datetime import datetime, timedelta

from config import BaseApiConfig
from src.api.pool.services.location_services import LocationFormService
from src.api.pool.services.meeting_services.meeting_time_services.meeting_location_service import MeetingLocationService
from src.message_queue.tasks.email_tasks.base_email_task import BaseEmailTask
from src.message_queue.tasks.email_tasks.email_factory.excel_writer.schedule_writer import ScheduleWriter


class AttachXLSTask(BaseEmailTask):
    __xls = []
    __location_ids = []
    __NOW = datetime.now() + timedelta(hours=BaseApiConfig.TIME_DIFFERENCE)
    __location_names = []

    def _addition_init(self, *args, **kwargs):
        self.__location_ids = kwargs.get('location_ids', [])
        self.__from_date = kwargs.get('from_date', self.__NOW + timedelta(days=-7))
        self.__to_date = kwargs.get('to_date', self.__NOW + timedelta(days=7))

        # celery modify date time to string ---> need to secure data type
        if isinstance(self.__from_date, str):
            self.__from_date = datetime.strptime(self.__from_date, '%Y-%m-%dT%H:%M:%S')
        if isinstance(self.__to_date, str):
            self.__to_date = datetime.strptime(self.__to_date, '%Y-%m-%dT%H:%M:%S')

        self.__f_date = datetime.strftime(self.__from_date, '%d-%m-%Y')
        self.__t_date = datetime.strftime(self.__to_date, '%d-%m-%Y')

    def _create_text_body(self) -> str:
        txt_body = 'Tổng hợp lịch họp: {f_date} đến {t_date} tại'.format(
            f_date=self.__f_date, t_date=self.__t_date
        )
        index = 1
        for location_name in self.__location_names:
            txt_body += ' {}'.format(location_name)
            if self.__location_names[0]:
                txt_body += ','
            else:
                txt_body += '.'
            index += 1
        return txt_body

    def _create_email_subject(self) -> str:
        return 'vMeeting: {f_date} đến {t_date}'.format(
            f_date=self.__f_date, t_date=self.__t_date
        )

    def _create_attachment_paths(self) -> list:
        self.__create_xsl()
        return [
            *self.__xls
        ]

    def __create_xsl(self):
        meeting_service = self._prepared_service(base_service=MeetingLocationService())
        location_service = self._prepared_service(base_service=LocationFormService())

        if isinstance(meeting_service, MeetingLocationService):
            writer = ScheduleWriter()

            for location_id in self.__location_ids:
                location = location_service.get_model(_id=location_id)
                self.__location_names.append(location.name)
                meetings = meeting_service.get_location_meetings(location_id=location_id,
                                                                 from_date=self.__from_date,
                                                                 to_date=self.__to_date)

                writer.init_location(**{
                    'location_name': location.name,
                    'from': self.__from_date,
                    'to': self.__to_date,
                    'meetings': meetings
                })
                self.__xls.append({
                    'path': writer.export(export_name='vMeeting_' + self.__f_date + ':' + self.__t_date)})
