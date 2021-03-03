from . import CommonString, StringValidator


class ShortString(CommonString):
    @staticmethod
    def _string_filter_rules() -> list:
        return [ShortStringValidator]


class ShortStringValidator(StringValidator):
    __SHORT_LEN = 50
    __ERR_MSG = 'String length must be shorter than {} characters.'.format(__SHORT_LEN)

    def _do_validate(self, validated_str: str) -> bool:
        return len(validated_str) < self.__SHORT_LEN

    def _create_error_message(self) -> str:
        return self.__ERR_MSG
