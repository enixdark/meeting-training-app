from . import CommonUnsignedInteger, UnsignedIntegerValidator


class MediumUnsignedInteger(CommonUnsignedInteger):
    @staticmethod
    def _unsigned_integer_filter_rules() -> list:
        return [MediumUnsignedIntegerValidator]


class MediumUnsignedIntegerValidator(UnsignedIntegerValidator):
    __MEDIUM_INT = 16777215
    __ERR_MSG = 'Must be less than or equal to {}.'.format(__MEDIUM_INT)

    def _do_validate(self, validated_integer: int) -> bool:
        return validated_integer <= self.__MEDIUM_INT

    def _create_error_message(self) -> str:
        return self.__ERR_MSG
