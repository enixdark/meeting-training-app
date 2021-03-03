from datetime import datetime, timedelta

from sqlalchemy import true, false, text
from sqlalchemy.orm import subqueryload

from config import BaseApiConfig
from src.api.pool.services import FormService, DecoratorService, InstantFormService
from src.database.postgres.meeting import Meeting


class MeetingFormService(FormService):
    def __init__(self):
        super().__init__()
        self.__now = datetime.now() + timedelta(hours=int(BaseApiConfig.TIME_DIFFERENCE))

    def create_many_to_many_relations(self) -> dict:
        return {
            'attendees': 'associate_users'
        }

    def _create_class_model(self):
        return Meeting

    # get meetings from today to future
    def get_available_meetings(self, location_id=None, limit=10):
        query = self.session.query(Meeting) \
            .filter(Meeting.finished_time >= self.__now,
                    Meeting.state == true()) \
            .order_by(Meeting.started_time)
        if location_id:
            query = query.filter_by(location_id=location_id)
        return query.limit(limit).all()

    # get meetings on-going meetings
    def get_going_meetings(self, location_id=None, limit=10):
        query = self.session.query(Meeting) \
            .filter(Meeting.finished_time >= self.__now,
                    Meeting.started_time < self.__now,
                    Meeting.state == true()) \
            .order_by(Meeting.started_time)
        if location_id:
            query = query.filter_by(location_id=location_id)
        return query.limit(limit).all()

    # get meeting from yesterday to the past
    def get_happened_meetings(self, location_id=None, limit=10):
        query = self.session.query(Meeting) \
            .filter(Meeting.finished_time < self.__now) \
            .order_by(Meeting.started_time)
        if location_id:
            query = query.filter_by(location_id=location_id)
        return query.limit(limit).all()

    # get meetings from tomorrow to future
    def get_future_meetings(self, location_id=None, limit=10):
        query = self.session.query(Meeting) \
            .filter(Meeting.started_time >= self.__now.date() + timedelta(days=1)) \
            .order_by(Meeting.started_time)
        if location_id:
            query = query.filter_by(location_id=location_id)
        return query.limit(limit).all()

    # get today meetings
    def get_today_meetings(self, location_id=None, limit=10):
        query = self.session.query(Meeting) \
            .filter(
            Meeting.started_time > self.__now.date(),
            Meeting.started_time <= self.__now.date() + timedelta(days=1)) \
            .order_by(Meeting.started_time)
        if location_id:
            query = query.filter_by(location_id=location_id)
        return query.limit(limit).all()

    # get today meetings from now to the end of the day
    def get_available_today_meetings(self, location_id=None, limit=10):
        query = self.session.query(Meeting) \
            .filter(
            Meeting.started_time >= self.__now,
            Meeting.started_time < self.__now.date() + timedelta(days=1)) \
            .order_by(Meeting.started_time)
        if location_id:
            query = query.filter_by(location_id=location_id)
        return query.limit(limit).all()

    # get meeting on specific date
    def get_meetings_on_date(self, date=datetime.now().date(), location_id=None, limit=10):
        query = self.session.query(Meeting) \
            .filter(
            Meeting.started_time > date,
            Meeting.started_time <= date + timedelta(days=1),
            Meeting.state == true()) \
            .order_by(Meeting.started_time)
        if location_id:
            query = query.filter_by(location_id=location_id)
        return query.limit(limit).all()


class MeetingInstantFormService(InstantFormService):
    def _create_class_model(self):
        return Meeting


class MeetingDecoratorService(DecoratorService):
    def create_many_to_many_relations(self) -> dict:
        return {
            'attendees': 'associate_users'
        }

    def _create_class_model(self):
        return Meeting
