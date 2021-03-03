from . import BaseMeetingPeriodicCreateDecorator


class AdminPeriodicCreateDecorator(BaseMeetingPeriodicCreateDecorator):

    def _add_periodic_state(self, **kwargs) -> dict:
        kwargs['state'] = True
        kwargs['is_approval'] = True
        return kwargs
