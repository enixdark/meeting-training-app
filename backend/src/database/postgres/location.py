from sqlalchemy import Column, String, Boolean, Time, ForeignKey

from src.database.postgres.base import Model, Base


class Location(Base, Model):
    name = Column(String(200), nullable=False, unique=True)
    is_multi_access = Column(Boolean, nullable=False)
    opened_time = Column(Time, nullable=False)
    closed_time = Column(Time, nullable=False)
    address = Column(String(500), nullable=False)
    google_map_id = Column(String(50), unique=True)
    manager_id = Column(ForeignKey('user.id', ondelete='CASCADE'))
    need_approval = Column(Boolean, nullable=False)

    def _to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'is_multi_access': self.is_multi_access,
            'opened_time': self.opened_time.isoformat(),
            'closed_time': self.closed_time.isoformat(),
            'address': self.address,
            'google_map_id': self.google_map_id,
            'manager_id': self.manager_id,
            'need_approval': self.need_approval,
            # 'meetings': None
        }

    def _relation_keys(self) -> list:
        return ['meetings', 'manager']

    def _meetings(self):
        return [meeting.serialize() for meeting in self.meetings]

    def _manager(self):
        return self.manager.serialize(exclusion=['locations'])
