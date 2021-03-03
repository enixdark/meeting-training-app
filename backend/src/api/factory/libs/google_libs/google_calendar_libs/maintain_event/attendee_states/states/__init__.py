from abc import ABC, abstractmethod


class AttendeeState(ABC):
    @abstractmethod
    def state_message(self) -> str:
        pass
