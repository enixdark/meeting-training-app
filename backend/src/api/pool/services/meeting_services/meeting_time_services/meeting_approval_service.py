from sqlalchemy import text, false
from sqlalchemy.orm import subqueryload

from src.api.pool.services.meeting_services.meeting_time_services import MeetingTimeService, Meeting


class MeetingApprovalService(MeetingTimeService):
    def get_approval_meetings(self, *args, **kwargs):
        sort = kwargs.get('sort', Meeting.created_at)
        order = kwargs.get('order', 'desc')
        offset_n = kwargs.get('offset', 0)
        limit_n = kwargs.get('limit', 5)

        query = self.session.query(Meeting) \
            .options(subqueryload(Meeting.associate_users)) \
            .filter(Meeting.is_approval == false(),
                    Meeting.started_time > self._NOW)
        if order == 'desc':
            from sqlalchemy import desc
            query = query.order_by(desc(text(sort)))
        else:
            query = query.order_by(text(sort))
        query = query.offset(offset_n)
        query = query.limit(limit_n)

        return query.all()

    def get_duplicated_meeting(self, meeting: Meeting):
        query = self.session.query(Meeting) \
            .filter(
            Meeting.id != meeting.id,
            Meeting.started_time <= meeting.started_time,
            Meeting.finished_time > meeting.started_time,
            Meeting.location_id == meeting.location_id
        )
        return query.all()