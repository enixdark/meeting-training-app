from src.api.pool.services.attendee_services import AttendeeFormService
from src.api.pool.decorators.attendee_decorators.confirm_decorator.affirmative_confirm_decorator import \
    AttendeeConfirmDecorator
from src.api.pool.decorators.celery_decorator import CeleryDecorator
from src.message_queue.tasks.calendar_tasks import ConfirmEventTask
from src.message_queue.tasks.email_tasks import ConfirmEmailTask


class AttendeeCalendarConfirmDecorator(CeleryDecorator):
    def __init__(self):
        super(AttendeeCalendarConfirmDecorator, self).__init__()
        self.__confirm_decorator = None

    def set_confirm_decorator(self, confirm_decorator: AttendeeConfirmDecorator):
        self.__confirm_decorator = confirm_decorator

    def update_model(self, *args, **kwargs) -> bool:
        meeting_id = kwargs['meeting_id']
        auth_user = self.get_authenticated_user()

        # update confirm meeting to database
        self.__confirm_decorator.set_authenticated_user(auth_user_id=auth_user.id)
        updated = self.__confirm_decorator.update_model(*args, **kwargs)

        # set calendar celery task
        self._add_executor(task=ConfirmEventTask(),
                           delay_arguments={
                               'meeting_id': meeting_id,
                               'user_id': auth_user.id
                           })
        # set email celery task
        meeting_coordinator = AttendeeFormService().get_meeting_coordinator(meeting_id)
        self._add_executor(task=ConfirmEmailTask(),
                           delay_arguments={
                               'meeting_id': meeting_id,
                               'received_email': meeting_coordinator.user.email,
                               'confirm_name': auth_user.name,
                               'confirm_email': auth_user.email,
                               'confirm_status': self.__confirm_decorator.get_email_status()
                           })
        self._execute()

        return updated
