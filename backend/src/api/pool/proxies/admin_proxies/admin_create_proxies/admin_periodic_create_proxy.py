from src.api.pool.decorators.meeting_decorators.meeting_celery_decorators.meeting_calendar_task_decorator.meeting_calendar_create_decorators.admin_periodic_calendar_create_decorator import \
    AdminPeriodicCalendarCreateDecorator
from src.api.pool.proxies.admin_proxies.admin_create_proxies import AdminCreateProxy
from src.api.pool.services import Service


class AdminPeriodicMeetingCreateProxy(AdminCreateProxy):
    def _create_service(self) -> Service:
        return AdminPeriodicCalendarCreateDecorator()
