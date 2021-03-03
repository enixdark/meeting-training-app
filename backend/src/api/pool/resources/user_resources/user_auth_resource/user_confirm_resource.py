from src.api.pool.decorators.attendee_decorators.attendee_celery_decorators.attendee_calendar_confirm_decorator import \
    AttendeeCalendarConfirmDecorator
from src.api.pool.decorators.attendee_decorators.confirm_decorator.affirmative_confirm_decorator import \
    AttendeeAffirmativeDecorator
from src.api.pool.decorators.attendee_decorators.confirm_decorator.negative_confirm_decorator import \
    AttendeeNegativeDecorator
from src.api.pool.decorators.attendee_decorators.confirm_decorator.uncertain_confirm_decorator import \
    AttendeeUncertainDecorator
from ... import BaseAPI, Resource, Request
from ...authenticated_resources.auth_resource import AuthenticatedDecorator, BaseAuthenticatedResource
from ...entities.requests.implement_requests.attendee_requests.confirm_meeting_request import AttendeeConfirmRequest
from src.api.pool.resources.entities.responses.implement_responses.method_responses.update_responses.confirm_responses import ConfirmUpdateSuccessResponse


class UserConfirmAuthResource(BaseAuthenticatedResource):
    def _create_service(self) -> AuthenticatedDecorator:
        return AttendeeAffirmativeDecorator()

    def post(self, request: Request, *args, **kwargs):
        confirm_status = request.get('confirm_status')
        celery_decorator = AttendeeCalendarConfirmDecorator()
        if confirm_status == 'uncertain':
            self._set_service(AttendeeUncertainDecorator())
        if confirm_status == 'negative':
            self._set_service(AttendeeNegativeDecorator())
        # set authentication to the authenticated service
        celery_decorator.set_confirm_decorator(self._service)
        self._set_service(celery_decorator)
        self._set_up_authenticate_service(request)

        self._service.update_model(**request.all())
        self._set_response(ConfirmUpdateSuccessResponse())

        return [True]


class UserConfirmAuthAPI(BaseAPI):
    def _create_resource(self) -> Resource:
        return UserConfirmAuthResource()

    POST = {
        'request': AttendeeConfirmRequest
    }
