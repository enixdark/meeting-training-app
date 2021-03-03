from src.api.pool.decorators.meeting_decorators.meeting_celery_decorators.meeting_calendar_task_decorator.meeting_calendar_delete_decorators.periodic_calendar_delete_decorator import \
    PeriodicCalendarDeleteDecorator
from src.api.pool.proxies.meeting_coordinator_proxies.coordinator_delete_proxies import CoordinatorDeleteProxy
from src.api.pool.services import Service


class CoordinatorPeriodicDeleteProxy(CoordinatorDeleteProxy):
    def _create_service(self) -> Service:
        return PeriodicCalendarDeleteDecorator()

    def get_delete_service(self) -> PeriodicCalendarDeleteDecorator:
        return self._get_service()
