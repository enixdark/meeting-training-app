from abc import ABC, abstractmethod


class MeetingLocation(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs) -> bool:
        pass
