from src.api.factory.libs.google_libs.google_account_libs import GoogleUserService, GoogleCheckDomainService
from src.api.pool.decorators.user_decorators import UserDecorator
from src.api.pool.services.role_services import RoleFormService
from src.database.postgres.base import Model


class TokenLoginDecorator(UserDecorator):
    def find_model(self, pairs: dict, **kwargs) -> Model:
        google_service = GoogleUserService()
        google_response = google_service.execute(**kwargs)
        # if exchange user data successfully
        if google_response.status:
            user_info = google_response.data
            email = user_info['email']
            google_email_service = GoogleCheckDomainService()
            google_response = google_email_service.execute(email=email)
            # if email domain is valid
            if google_response.status:
                user = super().find_model(pairs={'email': email})
                if user:
                    self.update_model(_id=user.id, name=user_info['name'],
                                      email=user_info['email'],
                                      refresh_token=kwargs.get('refresh_token', None),
                                      access_token=kwargs.get('access_token', None),
                                      avatar_url=user_info['picture'],
                                      is_activated=True)
                else:
                    user = self.create_new_model(
                        name=user_info['name'],
                        email=user_info['email'],
                        refresh_token=kwargs.get('refresh_token', None),
                        access_token=kwargs.get('access_token', None),
                        avatar_url=user_info['picture'],
                        is_activated=True,
                    )
                    role_service = RoleFormService()
                    role_user = role_service.find_model(pairs={'role_type': 'user'})
                    user.roles = [role_user]
                self.commit()
                return user
