from . import CommonUnsignedInteger, UnsignedIntegerValidator


class TinyUnsignedInteger(CommonUnsignedInteger):
    @staticmethod
    def _unsigned_integer_filter_rules() -> list:
        return [TinyUnsignedIntegerValidator]


class TinyUnsignedIntegerValidator(UnsignedIntegerValidator):
    __TINY_INT = 255
    __ERR_MSG = 'Must be less than or equal to {}.'.format(__TINY_INT)

    def _do_validate(self, validated_integer: int) -> bool:
        return validated_integer <= self.__TINY_INT

    def _create_error_message(self) -> str:
        return self.__ERR_MSG
