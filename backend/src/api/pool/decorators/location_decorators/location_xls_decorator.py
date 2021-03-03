from src.api.pool.decorators.celery_decorator import CeleryDecorator
from src.api.pool.decorators.decorator_helpers.decorator_counters.xls_decorator_counter import XLSDecoratorCounter
from src.api.pool.services import Service
from src.api.pool.services.location_services import LocationFormService
from src.message_queue.tasks.email_tasks import AttachXLSTask
from src.message_queue.tasks.email_tasks.remove_file_task import RemoveFileTask


class LocationXLSDecorator(CeleryDecorator):
    def __init__(self):
        super(LocationXLSDecorator, self).__init__()
        self.__counter = XLSDecoratorCounter()

    def get_all(self, *args, **kwargs):
        auth_user = self.get_authenticated_user()
        raw_location_ids = kwargs['nested']
        location_ids = []

        index = 0
        for location_id in raw_location_ids:
            location_id = location_id['id']
            location = self.get_model(_id=location_id)
            if location:
                location_ids.append(location_id)
                self.__counter.update_success_states(update_index=index)
            else:
                self.__counter.update_failed_states(update_index=index, failed_reason='Invalid location id')
            index += 1

        self._add_executor(task=AttachXLSTask(),
                           delay_arguments={
                               'meeting_id': 0,
                               'received_email': auth_user.email,
                               'location_ids': location_ids,
                               'from_date': kwargs.get('from_date', None),
                               'to_date': kwargs.get('to_date', None)
                           })
        self._add_executor(task=RemoveFileTask(),
                           delay_arguments={
                               'from_date': kwargs.get('from_date', None),
                               'to_date': kwargs.get('to_date', None)
                           })
        self._execute_chain()

    def get_xls_messages(self) -> dict:
        return self.__counter.get_periodic_messages()

    def get_success_count(self) -> int:
        return self.__counter.get_success_count()

    def get_failed_count(self) -> int:
        return self.__counter.get_failed_count()

    def _create_service(self) -> Service:
        return LocationFormService()
