from . import CommonUnsignedInteger, UnsignedIntegerValidator


class SmallUnsignedInteger(CommonUnsignedInteger):
    @staticmethod
    def _unsigned_integer_filter_rules() -> list:
        return [SmallUnsignedIntegerValidator]


class SmallUnsignedIntegerValidator(UnsignedIntegerValidator):
    __SMALL_INT = 65535
    __ERR_MSG = 'Must be less than or equal to {}.'.format(__SMALL_INT)

    def _do_validate(self, validated_integer: int) -> bool:
        return validated_integer <= self.__SMALL_INT

    def _create_error_message(self) -> str:
        return self.__ERR_MSG
