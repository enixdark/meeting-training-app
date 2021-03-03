from . import SingleUpdateSuccessResponse, SingleUpdateFailedResponse


class MeetingSynchronizedSuccessResponse(SingleUpdateSuccessResponse):
    def __init__(self):
        super().__init__()
        self.response_message = 'Synchronized.'


class MeetingNotSynchronizedResponse(SingleUpdateFailedResponse):
    def __init__(self):
        super().__init__()
        self.response_message = 'Not synchronized.'
