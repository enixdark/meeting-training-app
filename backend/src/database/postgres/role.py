from src.database.postgres.base import Model, Base
from sqlalchemy import Column, String


class Role(Base, Model):
    role_type = Column(String(50), nullable=False)

    def _to_dict(self) -> dict:
        return {
            'id': self.id,
            'role_type': self.role_type,
        }

    def _relation_keys(self) -> list:
        return ['users']

    def _users(self):
        return [user.serialize() for user in self.users]
