from src.api.pool.decorators.celery_decorator import CeleryDecorator, Service
from src.api.pool.decorators.meeting_decorators.meeting_create_decorators.meeting_approval_create_decorator import \
    MeetingApprovalCreateDecorator, Model
from src.api.pool.services.attendee_services import AttendeeFormService
from src.message_queue.tasks.calendar_tasks import CreateEventTask
from src.message_queue.tasks.email_tasks import InvitedEmailTask
from src.message_queue.tasks.email_tasks.retrieve_meeting_email_task.request_approval_email_task import \
    RequestApprovalEmailTask


class MeetingEmailApprovalCreateDecorator(CeleryDecorator):
    def _create_service(self) -> Service:
        return MeetingApprovalCreateDecorator()

    def create_new_model(self, *args, **kwargs) -> Model:
        new_meeting = super(MeetingEmailApprovalCreateDecorator, self).create_new_model(*args, **kwargs)
        if new_meeting:
            # if meeting is created in a location that no need for approval from admin, send request email is not
            # necessary.
            if not new_meeting.is_approval:
                self._add_executor(task=RequestApprovalEmailTask(),
                                   delay_arguments={
                                       'meeting_id': new_meeting.id,
                                       'received_email': new_meeting.location.manager.email
                                   })
            else:
                # else, send email to all attendees and use coordinator access_token to create Google calendar event
                attendee_service = AttendeeFormService()
                coordinator = attendee_service.get_meeting_coordinator(meeting_id=new_meeting.id)
                for attendee in new_meeting.associate_users:
                    if attendee.user_id is not coordinator.user_id:
                        self._add_executor(task=InvitedEmailTask(),
                                           delay_arguments={
                                               'meeting_id': new_meeting.id,
                                               'received_email': attendee.user.email
                                           })
                self._add_executor(task=CreateEventTask(),
                                   delay_arguments={
                                       'meeting_id': new_meeting.id,
                                       'user_id': coordinator.user_id
                                   })
            self._execute()
        return new_meeting
