from . import CommonUnsignedInteger, UnsignedIntegerValidator


class UnsignedInteger(CommonUnsignedInteger):
    @staticmethod
    def _unsigned_integer_filter_rules() -> list:
        return [NormalUnsignedIntegerValidator]


class NormalUnsignedIntegerValidator(UnsignedIntegerValidator):
    __NORMAL_INT = 4294967295
    __ERR_MSG = 'Must be less than or equal to {}.'.format(__NORMAL_INT)

    def _do_validate(self, validated_integer: int) -> bool:
        return validated_integer <= self.__NORMAL_INT

    def _create_error_message(self) -> str:
        return self.__ERR_MSG
