from . import AttendeeState


class AttendeeDeclinedState(AttendeeState):
    __DECLINED_MESSAGE = 'declined'

    def state_message(self) -> str:
        return self.__DECLINED_MESSAGE
