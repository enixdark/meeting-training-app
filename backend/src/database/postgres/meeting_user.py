from src.database.postgres.base import Model, Base
from sqlalchemy import Column, ForeignKey, Boolean, Integer, String
from sqlalchemy.orm import relationship


class MeetingUser(Base, Model):
    meeting_id = Column(Integer, ForeignKey('meeting.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    is_accepted = Column(Boolean, nullable=False)
    is_response = Column(Boolean, nullable=False, default=False)
    may_join = Column(Boolean, nullable=False, default=False)
    is_coordinator = Column(Boolean, nullable=False)
    note = Column(String(200), nullable=True)

    user = relationship('User', back_populates='associate_meetings', single_parent=True, lazy='subquery')
    meeting = relationship('Meeting', back_populates='associate_users', single_parent=True, lazy='subquery')

    def _to_dict(self) -> dict:
        return {
            'is_accepted': self.is_accepted,
            'is_coordinator': self.is_coordinator,
            'is_response': self.is_response,
            'meeting_id': self.meeting_id,
            'user_id': self.user_id,
            'note': self.note,
            'may_join': self.may_join
        }

    def _relation_keys(self) -> list:
        return ['user', 'meeting']

    def _user(self):
        return self.user.serialize(exclusion=['id'])

    def _meeting(self):
        return self.meeting.serialize()
