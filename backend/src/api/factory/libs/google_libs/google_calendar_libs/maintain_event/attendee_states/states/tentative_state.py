from . import AttendeeState


class AttendeeTentativeState(AttendeeState):
    __TENTATIVE_MESSAGE = 'tentative'

    def state_message(self) -> str:
        return self.__TENTATIVE_MESSAGE
