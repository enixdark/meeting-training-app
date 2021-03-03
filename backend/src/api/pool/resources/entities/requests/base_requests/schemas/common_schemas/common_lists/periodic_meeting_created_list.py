from abc import ABC, abstractmethod

from src.api.pool.resources.entities.requests.base_requests.schemas.common_schemas.common_lists import CommonList, \
    CommonListValidator


class PeriodicMeetingCreatedList(CommonList):
    @staticmethod
    def _common_list_filter_rules() -> list:
        return [DistinctFinishedTimeValidator,
                DistinctStartedTimeValidator, ]


class DistinctTimeValidator(CommonListValidator, ABC):

    def _do_validate(self, validator_list: list) -> bool:
        list_len = len(validator_list)
        distinct_element = self._create_distinct_element_name()
        for i in range(list_len):
            for j in range(i + 1, list_len):
                if validator_list[i][distinct_element] == validator_list[j][distinct_element]:
                    return False
        return True

    @abstractmethod
    def _create_distinct_element_name(self) -> str:
        pass


class DistinctStartedTimeValidator(DistinctTimeValidator):
    __DISTINCT_ERR_MSG = "Elements's stated_time field must be distinct"
    __DISTINCT_ELEMENT_NAME = 'started_time'

    def _create_error_message(self) -> str:
        return self.__DISTINCT_ERR_MSG

    def _create_distinct_element_name(self) -> str:
        return self.__DISTINCT_ELEMENT_NAME


class DistinctFinishedTimeValidator(DistinctTimeValidator):
    __DISTINCT_ERR_MSG = "Elements's finished_time field must be distinct"
    __DISTINCT_ELEMENT_NAME = 'finished_time'

    def _create_error_message(self) -> str:
        return self.__DISTINCT_ERR_MSG

    def _create_distinct_element_name(self) -> str:
        return self.__DISTINCT_ELEMENT_NAME
