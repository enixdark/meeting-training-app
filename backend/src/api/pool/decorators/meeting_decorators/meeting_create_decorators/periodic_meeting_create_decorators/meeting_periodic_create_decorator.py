from src.api.pool.services.location_services import LocationFormService
from . import BaseMeetingPeriodicCreateDecorator


class MeetingPeriodicCreateDecorator(BaseMeetingPeriodicCreateDecorator):
    def _add_periodic_state(self, **kwargs) -> dict:
        location_service = LocationFormService()
        location = location_service.get_model(_id=kwargs['location_id'])
        if location:
            if not location.need_approval:
                kwargs['state'] = True
                kwargs['is_approval'] = True
            else:
                kwargs['state'] = False
                kwargs['is_approval'] = False
        return kwargs
