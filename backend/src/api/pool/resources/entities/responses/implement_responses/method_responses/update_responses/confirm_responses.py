from . import SingleUpdateSuccessResponse


class ConfirmUpdateSuccessResponse(SingleUpdateSuccessResponse):
    def __init__(self):
        super().__init__()
        self.response_message = 'Confirm successfully.'
