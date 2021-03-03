from . import UserDecorator


class UserSuggestDecorator(UserDecorator):
    def get_all(self, *args, **kwargs):
        email_query = kwargs.get('q', '')
        user_service = self._get_service()
        return user_service.get_similar_email_users(similar=email_query, **kwargs)
