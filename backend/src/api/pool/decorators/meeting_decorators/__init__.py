from src.api.pool.decorators import BaseDecorator, Service
from src.api.pool.services.meeting_services import MeetingFormService, MeetingDecoratorService
from ..auth_decorator import AuthenticatedDecorator


class MeetingDecorator(BaseDecorator):
    def _create_service(self) -> Service:
        return MeetingFormService()

    def _get_service(self) -> MeetingFormService:
        return super()._get_service()


class MeetingAuthDecorator(AuthenticatedDecorator):
    def _create_service(self) -> Service:
        return MeetingDecoratorService()

    def _get_service(self) -> MeetingDecoratorService:
        return super()._get_service()
