from src.api.pool.decorators.meeting_decorators.meeting_update_proxies import MeetingUpdateProxy
from src.api.pool.services.attendee_services import AttendeeFormService
from src.database.postgres.meeting_user import MeetingUser


class BaseMeetingCoordinatorUpdateProxy(MeetingUpdateProxy):
    def _check_update_authorization(self, *args, **kwargs) -> bool:
        """
        Check only the coordinator can update the meeting
        :return:
        """
        attendee_service = AttendeeFormService()
        coordinator = attendee_service.get_meeting_coordinator(kwargs['_id'])

        if isinstance(coordinator, MeetingUser):
            auth_user = self.get_authenticated_user()
            return coordinator.user_id == auth_user.id
        return False
