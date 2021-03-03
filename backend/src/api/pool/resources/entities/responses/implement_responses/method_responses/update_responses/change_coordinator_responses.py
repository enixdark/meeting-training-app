from . import SingleUpdateSuccessResponse


class CoordinatorUpdateSuccessResponse(SingleUpdateSuccessResponse):
    def __init__(self):
        super().__init__()
        self.response_message = 'Update coordinator successfully.'
