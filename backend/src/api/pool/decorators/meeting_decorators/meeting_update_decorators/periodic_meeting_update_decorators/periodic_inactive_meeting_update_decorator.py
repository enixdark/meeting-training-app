from src.api.pool.decorators.meeting_decorators.meeting_update_decorators.periodic_meeting_update_decorators import \
    BasePeriodicMeetingUpdateDecorator
from src.api.pool.services.meeting_services.periodic_meeting_services import PeriodicMeetingFormService
from src.api.pool.services.meeting_services.periodic_meeting_services.periodic_inactive_form_service import \
    PeriodicInactiveFormService


class PeriodicInactiveMeetingUpdateDecorator(BasePeriodicMeetingUpdateDecorator):
    def _create_periodic_service(self) -> PeriodicMeetingFormService:
        return PeriodicInactiveFormService()
