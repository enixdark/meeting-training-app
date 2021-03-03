from .change_coordinator_resource import ChangeCoordinatorAuthAPI
from .periodic_change_coordinator_resource import PeriodicChangeCoordinatorAuthAPI
from .user_confirm_resource import UserConfirmAuthAPI
from .user_log_resource import AttendeeLogAuthAPI

confirm_view = UserConfirmAuthAPI.as_view('confirm_api')
coordinator_view = ChangeCoordinatorAuthAPI.as_view('change_coordinator_api')
attendee_log_view = AttendeeLogAuthAPI.as_view('attendee_log_api')
periodic_coordinator_view = PeriodicChangeCoordinatorAuthAPI.as_view('periodic_change_coordinator_api')

user_prefix = 'user'

auth_user_routes = [
    {
        'uri': 'user/confirm',
        'view': confirm_view,
        'methods': ['POST', ]
    },
    {
        'uri': 'user/change_coordinator',
        'view': coordinator_view,
        'methods': ['PATCH', ]
    },
    {
        'uri': 'user/log',
        'view': attendee_log_view,
        'methods': ['GET', ]
    },
    {
        'uri': 'user/periodic/change_coordinator',
        'view': periodic_coordinator_view,
        'methods': ['PATCH', ]
    }

]
