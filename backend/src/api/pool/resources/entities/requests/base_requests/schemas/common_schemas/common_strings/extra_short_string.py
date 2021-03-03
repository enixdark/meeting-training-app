from . import CommonString, StringValidator


class ExtraShortString(CommonString):
    @staticmethod
    def _string_filter_rules() -> list:
        return [ExtraShortString]


class ExtraShortStringValidator(StringValidator):
    __EXTRA_SHORT_LEN = 5
    __ERR_MSG = 'String length must be shorter than {} characters.'.format(__EXTRA_SHORT_LEN)

    def _do_validate(self, validated_str: str) -> bool:
        return len(validated_str) <= self.__EXTRA_SHORT_LEN

    def _create_error_message(self) -> str:
        return self.__ERR_MSG
