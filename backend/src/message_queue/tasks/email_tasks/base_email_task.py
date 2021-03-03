from abc import abstractmethod

from config import BaseApiConfig
from src.api.factory.exceptions.service_exceptions.db_service_exceptions.meeting_exceptions import \
    InvalidMeetingIdException
from src.api.pool.services import BaseService
from src.api.pool.services.meeting_services import MeetingFormService
from src.database.postgres.meeting import Meeting
from src.message_queue.tasks.db_connection_task import DBConnectionTask
from src.message_queue.tasks.email_tasks.email_factory.html_mail_sender import MailSender


class BaseEmailTask(DBConnectionTask):
    meeting_id = 0
    received_email = 0
    __meeting = None

    def _create_service(self) -> BaseService:
        return MeetingFormService()

    def run(self, meeting_id: int, received_email: int, *args, **kwargs):
        # init
        print('SMTP task - {} is running!'.format(type(self).__name__))
        self.meeting_id = meeting_id
        self.received_email = received_email
        self._addition_init(*args, **kwargs)
        # send mail
        mail = self._create_email()
        self._send_mail(mail)
        # close session
        self.close_session()

    def _addition_init(self, *args, **kwargs):
        pass

    def _get_meeting(self) -> Meeting:
        if self.__meeting is None:
            self.__meeting = self._prepared_service().get_model(_id=self.meeting_id)
            if not isinstance(self.__meeting, Meeting):
                raise InvalidMeetingIdException()
        return self.__meeting

    def _create_email(self) -> dict:
        return {
            'to_addr': self.received_email,
            'gmail': False,
            'file_paths': self._create_attachment_paths(),
            'subject': self._create_email_subject(),
            'text_body': self._create_text_body(),
        }

    def _retrieve_meeting_information(self) -> dict:
        meeting = self._get_meeting()
        return meeting.serialize(inclusion_rs=['location'])

    @staticmethod
    def _create_attachment_paths() -> list:
        return []

    @staticmethod
    def _create_mail_sender() -> MailSender:
        return MailSender(**BaseApiConfig.EMAIL_CONFIG)

    def _send_mail(self, mail: dict):
        sender = self._create_mail_sender()
        sender.send(**mail)

    def _create_email_subject(self) -> str:
        return 'Untitled'

    def _create_text_body(self) -> str:
        return 'Nothing to show!!!'
