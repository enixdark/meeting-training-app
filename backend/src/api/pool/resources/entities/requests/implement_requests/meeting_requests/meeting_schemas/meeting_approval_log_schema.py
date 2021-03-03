from . import MeetingGetSchema


class MeetingApprovalLogSchema(MeetingGetSchema):
    def sort_rule(self) -> list:
        return [
            *super(MeetingApprovalLogSchema, self).sort_rule(),
            'started_time', 'created_at', 'updated_at'
        ]
