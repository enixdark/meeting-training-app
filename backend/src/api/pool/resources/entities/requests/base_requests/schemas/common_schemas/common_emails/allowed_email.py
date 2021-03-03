import re

from . import CommonEmail, EmailValidator


class AllowedDomainEmail(CommonEmail):
    @staticmethod
    def _email_filter_rules() -> list:
        return [DomainValidator]


class DomainValidator(EmailValidator):
    __ALLOWED_DOMAINS = ['vccorp.vn', 'gmail.com']
    __DOMAIN_REGEX = '(?<=@).*?$'
    __ERR_MSG = 'Email domain not allowed'

    def _do_validate(self, validated_email: str) -> bool:
        domain = re.search(self.__DOMAIN_REGEX, validated_email)
        return domain.group() in self.__ALLOWED_DOMAINS

    def _create_error_message(self) -> str:
        return self.__ERR_MSG
