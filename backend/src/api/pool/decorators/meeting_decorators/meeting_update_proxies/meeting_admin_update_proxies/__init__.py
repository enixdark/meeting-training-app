from src.api.pool.decorators.meeting_decorators.meeting_update_proxies import MeetingUpdateProxy


class BaseMeetingAdminUpdateProxy(MeetingUpdateProxy):
    def _check_update_authorization(self, *args, **kwargs) -> bool:
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
