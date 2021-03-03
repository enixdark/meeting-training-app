from src.api.pool.decorators.meeting_decorators.meeting_update_proxies.meeting_coordinator_update_proxies.periodic_meeting_coordinator_update_proxy import \
    PeriodicMeetingCoordinatorUpdateProxy
from src.api.pool.proxies.meeting_coordinator_proxies.coordinator_delete_proxies.coordinator_periodic_delete_proxy import \
    CoordinatorPeriodicDeleteProxy
from src.api.pool.resources.authenticated_resources.auth_resource import BaseAuthenticatedResource
from src.api.pool.resources.entities.requests.implement_requests.meeting_requests.periodic_meeting_delete_request import \
    PeriodicMeetingDeleteRequest
from src.api.pool.resources.entities.requests.implement_requests.meeting_requests.periodic_meeting_patch_request import \
    PeriodicMeetingPatchRequest
from src.api.pool.resources.entities.responses.implement_responses.method_responses.update_responses import \
    ListUpdateFailedResponse, \
    ListUpdateSuccessResponse, ListUpdatePartialResponse
from src.api.pool.resources.entities.responses.response_factories.list_response_factories import ListResponseFactory
from src.api.pool.resources.entities.responses.response_factories.list_response_factories.list_delete_response_factories.form_resource_delete_response_factory import \
    FormResourceDeleteResponseFactory
from src.api.pool.resources.entities.responses.response_factories.list_response_factories.list_patch_response_factories.form_resource_patch_response_factory import \
    FormResourcePatchResponseFactory
from .. import BaseAPI, Resource
from ..authenticated_resources.auth_form_resource import AuthenticatedDecorator, Request


class PeriodicMeetingAuthResource(BaseAuthenticatedResource):
    def _create_service(self) -> AuthenticatedDecorator:
        return PeriodicMeetingCoordinatorUpdateProxy()

    def patch(self, request: Request, *args, **kwargs):
        if isinstance(self._service, PeriodicMeetingCoordinatorUpdateProxy):
            # set auth user to auth service
            self._set_up_authenticate_service(request=request)

            # update multiple periodic meetings related to periodic meeting with input id
            request_data = request.all()
            _id = request_data.pop('id')
            self._service.update_model(_id=_id, **request_data)

            periodic_service = self._service.get_periodic_update_service()

            response_factory = self._create_update_response_factory()
            self._set_response(response_factory.get_response(success=periodic_service.get_success_count(),
                                                             failed=periodic_service.get_failed_count()))
            return periodic_service.get_periodic_messages()

    def delete(self, request: Request, *args, **kwargs):
        self._set_service(CoordinatorPeriodicDeleteProxy())
        if isinstance(self._service, CoordinatorPeriodicDeleteProxy):
            # set auth user to auth service
            self._set_up_authenticate_service(request=request)

            # update multiple periodic meetings related to periodic meeting with input id
            request_data = request.all()
            _id = request_data.pop('id')
            self._service.delete_model(_id=_id, **request_data)

            periodic_service = self._service.get_delete_service()
            response_factory = self._create_delete_response_factory()
            self._set_response(response_factory.get_response(success=periodic_service.get_success_count(),
                                                             failed=periodic_service.get_failed_count()))
            return periodic_service.get_delete_msg()

    @staticmethod
    def _create_delete_response_factory() -> ListResponseFactory:
        return FormResourceDeleteResponseFactory()

    @staticmethod
    def _create_update_response_factory() -> ListResponseFactory:
        return FormResourcePatchResponseFactory()


class PeriodicMeetingAuthAPI(BaseAPI):
    def _create_resource(self) -> Resource:
        return PeriodicMeetingAuthResource()

    PATCH = {
        'request': PeriodicMeetingPatchRequest
    }

    DELETE = {
        'request': PeriodicMeetingDeleteRequest
    }
