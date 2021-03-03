from src.database.postgres.base import Model, Base
from sqlalchemy import Column, String, Table, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship

association_table = Table('role_user', Base.metadata,
                          Column('user_id', Integer, ForeignKey('user.id')),
                          Column('role_id', Integer, ForeignKey('role.id')),
                          extend_existing=True,
                          )

from .role import Role
from .meeting import Meeting
from .meeting_user import MeetingUser


class User(Base, Model):
    name = Column(String(50))
    email = Column(String(200), nullable=False, unique=True)
    avatar_url = Column(String(200))
    access_token = Column(String(200))
    refresh_token = Column(String(200))
    is_activated = Column(Boolean)

    roles = relationship('Role', secondary=association_table, backref='users')
    meetings = relationship('Meeting', back_populates='creator', cascade="all, delete-orphan")
    associate_meetings = relationship('MeetingUser', back_populates='user', cascade="all, delete-orphan")
    managed_locations = relationship('Location', backref='manager')

    def _to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'avatar_url': self.avatar_url,
            'email': self.email,
        }

    def _relation_keys(self) -> list:
        return ['roles', 'host', 'attendants', 'locations']

    def _roles(self):
        return [role.serialize() for role in self.roles]

    def _host(self):
        return [meeting.serialize() for meeting in self.meetings]

    def _attendants(self):
        return [associated_meeting.serialize() for associated_meeting in self.associate_meetings]

    def _locations(self):
        return [managed_location.serialize() for managed_location in self.managed_locations]
