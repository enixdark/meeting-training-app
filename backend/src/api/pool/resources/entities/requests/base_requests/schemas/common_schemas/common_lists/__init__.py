from abc import ABC, abstractmethod
from marshmallow import fields

from src.api.pool.resources.entities.requests.base_requests.schemas.common_schemas import SchemaValidator, AdditionField


class CommonListValidator(SchemaValidator, ABC):
    @abstractmethod
    def _do_validate(self, validator_list: list) -> bool:
        pass


class CommonList(fields.List, AdditionField):
    def _validate(self, value):
        super(CommonList, self)._validate(value)
        self._validate_additions(value)

    def _create_addition_validators(self) -> list:
        return [
            *self._common_list_filter_rules(),
            MinimumLisLenValidator
        ]

    @staticmethod
    def _common_list_filter_rules() -> list:
        return []


class MinimumLisLenValidator(CommonListValidator):
    __MINIMUM_ERR_MSG = 'List has no item.'

    def _do_validate(self, validator_list: list) -> bool:
        return len(validator_list) > 0

    def _create_error_message(self) -> str:
        return self.__MINIMUM_ERR_MSG
