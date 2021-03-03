from config import BaseApiConfig
from src.api.pool.decorators.celery_decorator import CeleryDecorator, Service
from src.api.pool.decorators.meeting_decorators.meeting_celery_decorators.meeting_calendar_task_decorator.meeting_calendar_update_decorators.meeting_calendar_update_decorator import \
    MeetingCalendarUpdateDecorator
from src.message_queue.tasks.email_tasks import InformEmailTask, InvitedEmailTask


class MeetingEmailUpdateDecorator(CeleryDecorator):
    __DELAY_UPDATED_TIME = BaseApiConfig.EMAIL_UPDATE_DELAY

    def __init__(self):
        super(MeetingEmailUpdateDecorator, self).__init__()
        self.current_meeting_id = ''
        self.current_meeting_title = ''
        self.current_started_time = ''
        self.current_location_id = ''

    def _create_service(self) -> Service:
        return MeetingCalendarUpdateDecorator()

    def update_model(self, *args, **kwargs) -> bool:
        self._prepare_auth_service()
        current_meeting = self.get_model(_id=kwargs['_id'])
        self.current_meeting_id = current_meeting.id
        self.current_meeting_title = current_meeting.name
        self.current_started_time = current_meeting.started_time
        self.current_location_id = current_meeting.location_id

        if kwargs.get('attendees'):
            current_attendees = current_meeting.associate_users
        else:
            current_attendees = []

        updated = super(MeetingEmailUpdateDecorator, self).update_model(*args, **kwargs)

        updated_meeting = self.get_model(_id=kwargs['_id'])
        updated_attendees = updated_meeting.associate_users

        updated_email_attendees = self.__get_updated_attendees(current_attendees, updated_attendees)
        self.__send_updated_email(updated_email_attendees)

        if kwargs.get('attendees'):
            invited_email_attendees = self.__get_invited_attendees(current_attendees, updated_attendees)
            self.__send_invited_email(invited_email_attendees)

        self._execute()

        return updated

    def __send_updated_email(self, updated_email_attendees: list):
        for attendee in updated_email_attendees:
            if not attendee.is_coordinator:
                self._add_executor(task=InformEmailTask(),
                                   delay_arguments={
                                       'meeting_id': self.current_meeting_id,
                                       'received_email': attendee.user.email,
                                       'old_meeting_title': self.current_meeting_title,
                                       'old_started_time': self.current_started_time,
                                       'old_location_id': self.current_location_id
                                   },
                                   async_options={
                                       'countdown': self.__DELAY_UPDATED_TIME
                                   })

    def __send_invited_email(self, invited_email_attendees: list):
        for attendee in invited_email_attendees:
            if not attendee.is_coordinator:
                self._add_executor(task=InvitedEmailTask(),
                                   delay_arguments={
                                       'meeting_id': self.current_meeting_id,
                                       'received_email': attendee.user.email
                                   })

    @staticmethod
    def __get_invited_attendees(current_attendees, updated_attendees) -> list:
        invited_email_attendees = []
        for updated_attendee in updated_attendees:
            if updated_attendee not in current_attendees:
                invited_email_attendees.append(updated_attendee)

        return invited_email_attendees

    @staticmethod
    def __get_updated_attendees(current_attendees, updated_attendees) -> list:
        updated_email_attendees = []
        for current_attendee in current_attendees:
            if current_attendee not in updated_attendees:
                updated_email_attendees.append(current_attendee)

        return updated_email_attendees
