from abc import ABC, abstractmethod

from src.api.factory.exceptions.service_exceptions import ServiceException
from src.api.pool.services import FormService
from . import Resource, Request
from .entities.requests.base_requests.schema_requests.base_nested_requests import NestedPostRequest, NestedPatchRequest, \
    NestedDeleteRequest
from .entities.responses.response_factories.list_response_factories import ListResponseFactory
from .entities.responses.response_factories.list_response_factories.list_delete_response_factories.form_resource_delete_response_factory import \
    FormResourceDeleteResponseFactory
from .entities.responses.response_factories.list_response_factories.list_patch_response_factories.form_resource_patch_response_factory import \
    FormResourcePatchResponseFactory
from .entities.responses.response_factories.list_response_factories.list_post_response_factories.form_resource_post_response_factory import \
    FormResourcePostResponseFactory
from .entities.responses.response_factories.single_response_factories.form_resource_get_response_factory import \
    FormResourceGetResponseFactory, SingleResponseFactory


class BaseFormResource(Resource, ABC):
    @abstractmethod
    def _create_service(self) -> FormService:
        pass

    def get(self, request: Request, *args, **kwargs):
        relations = request.get('relations')
        _id = request.get('id')
        if _id:
            model = self._service.get_model(_id)
            response_factory = self._create_get_response_factory()
            if model:
                self._set_response(response_factory.get_response(is_success=True))
                return model.serialize(inclusion_rs=relations)
            self._set_response(response_factory.get_response(is_success=False))

    def post(self, request: Request, *args, **kwargs):
        new_models = {}
        errors = {}
        if isinstance(request, NestedPostRequest):
            nested = request.get_nested_data()
            count = 0
            for raw_data in nested:
                try:
                    new_model = self._service.create_new_model(**raw_data)
                    new_models.update({count: new_model.serialize()})
                except ServiceException as se:
                    errors.update({count: se.get_message()})
                finally:
                    count += 1
        return self.__response_many(success=new_models, failed=errors,
                                    response_factory=self._create_post_response_factory())

    def patch(self, request: Request, *args, **kwargs):
        updated_models = {}
        errors = {}
        if isinstance(request, NestedPatchRequest):
            nested = request.get_nested_data()
            count = 0
            for raw_data in nested:
                try:
                    _id = raw_data.pop('id')
                    self._service.update_model(_id=_id, **raw_data)
                    updated_models.update({count: 'Update successfully'})
                except ServiceException as se:
                    errors.update({count: se.get_message()})
                finally:
                    count += 1
        return self.__response_many(success=updated_models, failed=errors,
                                    response_factory=self._create_patch_response_factory())

    def delete(self, request: Request, *args, **kwargs):
        deleted_models = {}
        errors = {}
        if isinstance(request, NestedDeleteRequest):
            nested = request.get_nested_data()
            count = 0
            for raw_data in nested:
                try:
                    _id = raw_data.pop('id')
                    self._service.delete_model(_id=_id, **raw_data)
                    deleted_models.update({count: 'Delete successfully'})
                except ServiceException as se:
                    errors.update({count: se.get_message()})
                finally:
                    count += 1
        return self.__response_many(success=deleted_models, failed=errors,
                                    response_factory=self._create_delete_response_factory())

    def __response_many(self, success: dict, failed: dict, response_factory: ListResponseFactory) -> dict:
        success_count = len(success)
        failed_count = len(failed)

        self._set_response(response_factory.get_response(success=success_count, failed=failed_count))
        return {'success': success, 'error': failed}

    @staticmethod
    def _create_get_response_factory() -> SingleResponseFactory:
        return FormResourceGetResponseFactory()

    @staticmethod
    def _create_post_response_factory() -> ListResponseFactory:
        return FormResourcePostResponseFactory()

    @staticmethod
    def _create_patch_response_factory() -> ListResponseFactory:
        return FormResourcePatchResponseFactory()

    @staticmethod
    def _create_delete_response_factory() -> ListResponseFactory:
        return FormResourceDeleteResponseFactory()
