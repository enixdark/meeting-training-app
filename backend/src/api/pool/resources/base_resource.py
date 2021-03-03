from abc import ABC

from src.api.pool.services import FormService, DecoratorService
from . import Resource, Request, ServiceException
from .entities.requests.base_requests.schema_requests.base_get_requests.get_request import GetRequest
from .entities.requests.base_requests.schema_requests.base_modified_requests.patch_request import PatchRequest
from .entities.requests.base_requests.schema_requests.base_modified_requests.post_request import PostRequest
from src.api.pool.resources.entities.responses.implement_responses.method_responses.create_responses import SingleCreateSuccessResponse, SingleCreateErrorResponse
from src.api.pool.resources.entities.responses.implement_responses.method_responses.get_responses import ResourceGetSuccessResponse, ResourceNotFoundResponse
from src.api.pool.resources.entities.responses.implement_responses.method_responses.update_responses import SingleUpdateSuccessResponse, SingleUpdateFailedResponse


class BaseResource(Resource, ABC):

    def get(self, request: GetRequest, *args, **kwargs):
        relations = request.get('relations')
        _id = request.get('id')
        if _id:
            model = self._service.get_model(_id)
            if model:
                self._set_response(ResourceGetSuccessResponse())
                return model.serialize(inclusion_rs=relations)
            self._set_response(ResourceNotFoundResponse())

    def post(self, request: PostRequest, *args, **kwargs):
        if isinstance(request, PostRequest):
            try:
                new_model = self._service.create_new_model(**request.all())
                self._set_response(SingleCreateSuccessResponse())
                return new_model
            except ServiceException as se:
                self._set_response(SingleCreateErrorResponse())
                return {0: se.get_message()}

    def patch(self, request: PatchRequest, *args, **kwargs):
        try:
            _id = request.get('id')
            updated_status = False
            if isinstance(self._service, FormService):
                updated_status = self._service.update_model(_id=_id, **request.all())
            elif isinstance(self._service, DecoratorService):
                model = self._service.get_model(_id=_id)
                updated_status = self._service.update_model(model, **request.all())
            if updated_status:
                self._set_response(SingleUpdateSuccessResponse())
            else:
                self._set_response(SingleUpdateFailedResponse())
            return updated_status
        except ServiceException as se:
            self._set_response(SingleUpdateFailedResponse())
            return {0: se.get_message()}

    def delete(self, request: Request, *args, **kwargs):
        pass
