from sqlalchemy import true

from src.api.pool.services import FormService, DecoratorService, InstantFormService
from src.database.postgres.user import User


class UserFormService(FormService):
    def create_many_to_many_relations(self) -> dict:
        return {
            'roles': 'roles',
            'attendants': 'associate_meetings'
        }

    def _create_class_model(self):
        return User

    def get_similar_email_users(self, similar: str, **kwargs):
        sort = kwargs.get('sort', None)
        order = kwargs.get('order', None)
        offset_number = kwargs.get('offset', None)
        limit_number = kwargs.get('limit', 5)

        pattern = '{}%'.format(similar)

        query = self.session.query(User) \
            .filter(User.is_activated == true(), User.email.like(pattern))
        if sort:
            if order == 'desc':
                from sqlalchemy import desc
                query = query.order_by(desc(sort))
            query = query.order_by(sort)
        if offset_number:
            query = query.offset(offset_number)

        return query.limit(limit_number).all()


class UserDecoratorService(DecoratorService):
    def _create_class_model(self):
        return User


class UserInstantFormService(InstantFormService):
    def _create_class_model(self):
        return User
