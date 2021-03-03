from src.api.pool.decorators.celery_decorator import CeleryDecorator


class AttendeeCeleryDecorator(CeleryDecorator):
    def __int__(self):
        super().__init__()
        self.__confirm_decorator = None
        self.__celery_decorator = None

    def update_model(self, *args, **kwargs) -> bool:
        auth_user = self.get_authenticated_user()

        # update confirm meeting to database
        self.__confirm_decorator.set_authenticated_user(auth_user_id=auth_user.id)
        updated = self.__confirm_decorator.update_model(*args, **kwargs)

        # set celery task to execute
        self.__celery_decorator.set_authenticated_user(auth_user_id=auth_user.id)
        self.__celery_decorator.update_model(*args, **kwargs)
        
        return updated
