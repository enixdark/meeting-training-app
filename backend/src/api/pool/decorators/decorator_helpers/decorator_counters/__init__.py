from abc import ABC, abstractmethod


class DecoratorCounter(ABC):
    def __init__(self):
        self._success = 0
        self._failed = 0
        self._success_messages = {}
        self._failed_messages = {}

    @abstractmethod
    def _create_default_success_message(self) -> str:
        pass

    @abstractmethod
    def _create_default_failed_message(self) -> str:
        pass

    def update_success_states(self, update_index: int, success_msg=''):
        if len(success_msg) == 0:
            success_msg = self._create_default_success_message()
        self._success += 1
        self._success_messages.update({update_index: success_msg})

    def update_failed_states(self, update_index: int, failed_reason=''):
        if len(failed_reason) == 0:
            failed_reason = self._create_default_failed_message()
        self._failed += 1
        self._failed_messages.update({update_index: failed_reason})

    def get_periodic_messages(self) -> dict:
        return {
            'success': self._success_messages,
            'false': self._failed_messages
        }

    def get_success_count(self) -> int:
        return self._success

    def get_failed_count(self) -> int:
        return self._failed
