from src.api.pool.decorators.meeting_decorators import MeetingDecorator, Service
from src.api.pool.decorators.meeting_decorators.meeting_create_decorators.meeting_create_decorator import \
    MeetingCreateDecorator, Model
from src.api.pool.services.location_services import LocationFormService


class MeetingApprovalCreateDecorator(MeetingDecorator):
    def _create_service(self) -> Service:
        """
        Create a non-periodic meeting (is_periodic is set to False).
        :return: New non-periodic meeting
        """
        return MeetingCreateDecorator()

    def create_new_model(self, *args, **kwargs) -> Model:
        """
        New meeting need to wait for approval from location_manager
        All meeting create activities that use this service have default state and is_approval input data fields
        :param args:
        :param kwargs:
        :return: New meeting with state and is_approval equal to False
        """
        location_service = LocationFormService()
        location = location_service.get_model(_id=kwargs['location_id'])

        if location:
            if location.need_approval:
                kwargs['state'] = False
                kwargs['is_approval'] = False
            else:
                kwargs['state'] = True
                kwargs['is_approval'] = True

        return super(MeetingApprovalCreateDecorator, self).create_new_model(*args, **kwargs)
