from src.api.pool.decorators.meeting_decorators import MeetingDecorator
from src.api.pool.services.meeting_services.meeting_time_services.meeting_approval_service import MeetingApprovalService


class MeetingApprovalLogDecorator(MeetingDecorator):
    def get_all(self, *args, **kwargs):
        approval_meeting_service = MeetingApprovalService()
        approval_meetings = approval_meeting_service.get_approval_meetings(*args, **kwargs)

        # list of meeting approval requests
        approval_requests = []
        for approval_meeting in approval_meetings:
            approval_request = dict()
            approval_request['meeting'] = approval_meeting.serialize(inclusion_rs=kwargs.get('relations'))
            # set state of request, if in the duplicated requests have a state field equal to True,
            # approval activity is forbidden
            approval_request['may_request'] = True
            duplicated_meetings = approval_meeting_service.get_duplicated_meeting(meeting=approval_meeting)
            duplicates = []
            for duplicated_meeting in duplicated_meetings:
                if duplicated_meeting.state is True:
                    approval_request['may_request'] = False
                duplicates.append(duplicated_meeting.serialize())
            approval_request['duplicates'] = duplicates
            approval_requests.append(approval_request)

        return approval_requests
