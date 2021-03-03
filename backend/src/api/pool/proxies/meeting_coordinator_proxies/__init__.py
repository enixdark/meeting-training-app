from abc import ABC, abstractmethod

from src.api.pool.decorators.meeting_decorators import MeetingAuthDecorator
from src.api.pool.proxies import Proxy
from src.api.pool.services.attendee_services import AttendeeFormService, MeetingUser


class CoordinatorProxy(Proxy, ABC):
    def _check_authorization(self, meeting_id: int) -> bool:
        """
        Check only the coordinator can update the meeting
        :return:
        """
        attendee_service = AttendeeFormService()
        coordinator = attendee_service.get_meeting_coordinator(meeting_id)

        if isinstance(coordinator, MeetingUser):
            auth_user = self.get_authenticated_user()
            return coordinator.user_id == auth_user.id
        return False
