from src.api.pool.decorators.meeting_decorators import MeetingDecorator


class ListMeetingDecorator(MeetingDecorator):
    def get_all(self, *args, **kwargs):
        meeting_service = self._get_service()
        location_id = kwargs.get('location_id', None)
        limit = kwargs.get('limit', None)
        future_meetings = meeting_service.get_future_meetings(location_id=location_id, limit=limit)
        on_going_meeting = meeting_service.get_going_meetings(location_id=location_id, limit=limit)
        today_meeting = meeting_service.get_available_today_meetings(location_id=location_id, limit=limit)
        return \
            {
                'futures': [meeting.serialize(inclusion_rs=kwargs['relations']) for meeting in future_meetings]
                ,
                'on_goings':
                    [meeting.serialize(inclusion_rs=kwargs['relations']) for meeting in on_going_meeting],
                'today':
                    [meeting.serialize(inclusion_rs=kwargs['relations']) for meeting in today_meeting],

            }
