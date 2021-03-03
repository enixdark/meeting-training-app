from . import ResourceListSuccessResponse


class AttendeeLogResourceResponse(ResourceListSuccessResponse):
    def __init__(self):
        super().__init__()
        self.response_message = 'Attendees log found.'
