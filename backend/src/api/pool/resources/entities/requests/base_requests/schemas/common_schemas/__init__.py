from abc import ABC, abstractmethod

from marshmallow import ValidationError


class AdditionField:
    @staticmethod
    def _create_addition_validators() -> list:
        return []

    def _validate_additions(self, value):
        errors = []
        kwargs = {}
        validators = self._create_addition_validators()
        for validator in validators:
            try:
                validator(value).validate()
            except ValidationError as err:
                kwargs.update(err.kwargs)
                if isinstance(err.messages, dict):
                    errors.append(err.messages)
                else:
                    errors.extend(err.messages)
        if errors:
            print(errors)
            raise ValidationError(errors, **kwargs)


class SchemaValidator(ABC):
    __DEFAULT_ERR_MSG = 'Validation failed'

    def __init__(self, value):
        self.__value = value

    def validate(self):
        result = self._do_validate(self.__value)
        if not result:
            raise ValidationError(self._create_error_message())
        return True

    @abstractmethod
    def _do_validate(self, value) -> bool:
        pass

    def _create_error_message(self) -> str:
        err_msg = '{error_msg} on {class_name}'.format(error_msg=self.__DEFAULT_ERR_MSG,
                                                       class_name=self.__class__.__name__)
        return err_msg
