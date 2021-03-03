from src.database.postgres.base import Model, Base
from sqlalchemy import Column, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship, backref

from .location import Location


class Meeting(Base, Model):
    name = Column(String(200), nullable=False)
    description = Column(String(5000), nullable=False)
    creator_id = Column(ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    is_periodic = Column(Boolean, nullable=False, default=False)
    state = Column(Boolean, nullable=False, default=False)
    location_id = Column(ForeignKey('location.id', ondelete='CASCADE'), nullable=False)
    started_time = Column(DateTime, nullable=False)
    finished_time = Column(DateTime, nullable=False)
    google_calendar_id = Column(String(50), nullable=True)
    must_synchronized = Column(Boolean, default=True, onupdate=True)
    periodic_id = Column(String(50), nullable=True)
    is_approval = Column(Boolean, nullable=True, default=False)

    creator = relationship('User', back_populates='meetings', single_parent=True)
    location = relationship('Location', backref=backref('meetings', cascade="all, delete-orphan", single_parent=True))
    associate_users = relationship('MeetingUser', back_populates='meeting', cascade="all, delete-orphan")

    def _to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_periodic': self.is_periodic,
            'state': self.state,
            'started_time': self.started_time.isoformat(),
            'finished_time': self.finished_time.isoformat(),
            'location_id': self.location_id,
            'creator_id': self.creator_id,
            'must_synchronized': self.must_synchronized,
            'is_approval': self.is_approval
        }

    def _relation_keys(self) -> list:
        return ['creator', 'location', 'attendees']

    def _creator(self):
        return self.creator.serialize()

    def _location(self):
        return self.location.serialize()

    def _attendees(self):
        return [user.serialize(inclusion_rs=['user']) for user in self.associate_users]
