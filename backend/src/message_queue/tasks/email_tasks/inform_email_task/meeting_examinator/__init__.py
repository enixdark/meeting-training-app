from abc import ABC, abstractmethod


class MeetingExaminator(ABC):
    @abstractmethod
    def state_message(self, *args, **kwargs) -> str:
        pass
