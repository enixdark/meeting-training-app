from . import ResourceGetResponse, ResourceListSuccessResponse


class MeetingDataResourceResponse(ResourceGetResponse):
    def __init__(self):
        super().__init__()
        self.response_message = 'Meeting found.'

    def serialize(self) -> dict:
        return {
            **super().serialize(),
            'count': 1
        }


class MeetingListResourceResponse(ResourceListSuccessResponse):
    def __init__(self):
        super().__init__()
        self.response_message = 'Meetings found.'

    def serialize(self) -> dict:
        return {
            **super().serialize(),
            'count_futures': len(self.response_data['futures']),
            'count_today': len(self.response_data['today']),
            'count_on_goings': len(self.response_data['on_goings']),
        }


class MeetingListErrorResourceResponse(ResourceListSuccessResponse):
    def __init__(self):
        super().__init__()
        self.response_code = 404
        self.response_message = 'Meeting len is 0.'


class MeetingCheckResourceResponse(ResourceGetResponse):
    def __init__(self):
        super().__init__()
        self.response_message = 'Meetings checked.'

    def serialize(self) -> dict:
        return {
            **super().serialize(),
            'count': len(self.response_data)
        }


class MeetingApprovalLogResponse(ResourceListSuccessResponse):
    def __init__(self):
        super(MeetingApprovalLogResponse, self).__init__()
        self.response_message = 'List of approval requests'

