from . import CommonString, StringValidator


class ExtraLongString(CommonString):
    @staticmethod
    def _string_filter_rules() -> list:
        return [ExtraLongStringValidator]


class ExtraLongStringValidator(StringValidator):
    __EXTRA_LONG_LEN = 5000
    __ERR_MSG = 'String length must be shorter than {} characters.'.format(__EXTRA_LONG_LEN)

    def _do_validate(self, validated_str: str) -> bool:
        return len(validated_str) < self.__EXTRA_LONG_LEN

    def _create_error_message(self) -> str:
        return self.__ERR_MSG
