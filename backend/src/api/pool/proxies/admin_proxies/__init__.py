from abc import ABC

from src.api.pool.proxies import Proxy


class AdminProxy(Proxy, ABC):
    def _check_authorization(self) -> bool:
        """
        Check only the admin can update the meeting
        :return:
        """
        auth_user = self.get_authenticated_user()
        auth_user_roles = auth_user.roles
        for auth_user_role in auth_user_roles:
            if auth_user_role.role_type == 'admin':
                return True
        return False
