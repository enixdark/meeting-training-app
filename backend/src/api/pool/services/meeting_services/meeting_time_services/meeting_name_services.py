from datetime import timedelta

from src.api.pool.services.meeting_services.meeting_time_services import MeetingTimeService, Meeting


class MeetingNameService(MeetingTimeService):
    def count_meetings_by_name(self, similar_name, **kwargs) -> int:
        query = self.__get_query_meeting_by_name(similar_name, **kwargs)
        return query.count()

    def get_meetings_by_name(self, similar_name: str, **kwargs):
        sort = kwargs.get('sort', None)
        order = kwargs.get('order', None)
        offset_number = kwargs.get('offset', 0)
        limit_number = kwargs.get('limit', 5)

        query = self.__get_query_meeting_by_name(similar_name, **kwargs)
        if sort:
            if order == 'desc':
                from sqlalchemy import desc
                query = query.order_by(desc(sort))
            query = query.order_by(sort)
        query = query.offset(offset_number).limit(limit_number)

        return query.all()

    def __get_query_meeting_by_name(self, similar_name: str, **kwargs):
        le_datetime = kwargs.get('le', self._NOW.date() - timedelta(days=7))
        ge_datetime = kwargs.get('ge', self._NOW.date() + timedelta(days=7))

        pattern = '{}%'.format(similar_name)

        return self.session.query(Meeting).filter(Meeting.started_time >= ge_datetime,
                                                  Meeting.started_time <= le_datetime,
                                                  Meeting.name.like(pattern))