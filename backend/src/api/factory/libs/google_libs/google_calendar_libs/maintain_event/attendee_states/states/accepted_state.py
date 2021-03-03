from . import AttendeeState


class AttendeeAcceptedState(AttendeeState):
    __ACCEPTED_MESSAGE = 'accepted'

    def state_message(self) -> str:
        return self.__ACCEPTED_MESSAGE
