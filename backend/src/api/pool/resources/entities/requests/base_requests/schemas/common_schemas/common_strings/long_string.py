from . import CommonString, StringValidator


class LongString(CommonString):
    @staticmethod
    def _string_filter_rules() -> list:
        return [LongStringValidator]


class LongStringValidator(StringValidator):
    __LONG_LEN = 500
    __ERR_MSG = 'String length must be shorter than {} characters.'.format(__LONG_LEN)

    def _do_validate(self, validated_str: str) -> bool:
        return len(validated_str) < self.__LONG_LEN

    def _create_error_message(self) -> str:
        return self.__ERR_MSG
