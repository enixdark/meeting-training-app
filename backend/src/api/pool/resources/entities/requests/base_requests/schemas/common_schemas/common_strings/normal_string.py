from . import CommonString, StringValidator


class NormalString(CommonString):
    @staticmethod
    def _string_filter_rules() -> list:
        return [NormalStringValidator]


class NormalStringValidator(StringValidator):
    __NORMAL_LEN = 200
    __ERR_MSG = 'String length must be shorter than {} characters.'.format(__NORMAL_LEN)

    def _do_validate(self, validated_str: str) -> bool:
        return len(validated_str) < self.__NORMAL_LEN

    def _create_error_message(self) -> str:
        return self.__ERR_MSG
