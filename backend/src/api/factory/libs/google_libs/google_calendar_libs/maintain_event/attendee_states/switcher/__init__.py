from ..states.tentative_state import AttendeeTentativeState
from ..states.accepted_state import AttendeeAcceptedState
from ..states.declined_state import AttendeeDeclinedState


class AttendeeStateSwitcher:
    def __init__(self):
        self.__state = None

    def get_state(self, is_accepted: bool, may_join: bool):
        if is_accepted:
            self.__state = AttendeeAcceptedState()
        elif may_join:
            self.__state = AttendeeTentativeState()
        else:
            self.__state = AttendeeDeclinedState()
        return self.__state.state_message()
