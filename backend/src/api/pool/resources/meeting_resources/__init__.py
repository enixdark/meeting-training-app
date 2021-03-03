from .meeting_auth_resource import MeetingAuthAPI
from .meeting_check_resource import CheckMeetingTimeAPI
from .meeting_list_resource import ListMeetingAPI
from .meeting_resource import MeetingAPI
from .meeting_synchronize_resource import SynchronizeMeetingAPI
from .periodic_meeting_auth_resource import PeriodicMeetingAuthAPI
from .meeting_admin_resources import admin_meeting_routes
from .meeting_approval_log_resource import CheckApprovalLogAPI
from .meeting_search_resource import MeetingSearchAPI

meeting_view = MeetingAPI.as_view('meeting_api')
meeting_auth_view = MeetingAuthAPI.as_view('meeting_auth_api')
list_meeting_view = ListMeetingAPI.as_view('list_meeting_api')
check_meeting_view = CheckMeetingTimeAPI.as_view('check_meeting_time_api')
synchronize_meeting_view = SynchronizeMeetingAPI.as_view('synchronize_meeting_api')
periodic_auth_view = PeriodicMeetingAuthAPI.as_view('periodic_patch_view')
approval_log_view = CheckApprovalLogAPI.as_view('approval_log_api')
meeting_search_view = MeetingSearchAPI.as_view('meeting_search_api')

meeting_routes = [
    {
        'uri': 'meeting/get',
        'view': meeting_view,
        'methods': ['GET', ]
    },
    {
        'uri': 'meeting/post',
        'view': meeting_auth_view,
        'methods': ['POST', ]
    },
    {
        'uri': 'meeting/patch',
        'view': meeting_auth_view,
        'methods': ['PATCH', ]
    },
    {
        'uri': 'meeting/delete',
        'view': meeting_auth_view,
        'methods': ['DELETE', ]
    },
    {
        'uri': 'meeting/delete',
        'view': meeting_view,
        'methods': ['DELETE', ]
    },
    {
        'uri': 'meeting/all',
        'view': list_meeting_view,
        'methods': ['GET', ]
    },
    {
        'uri': 'meeting/check',
        'view': check_meeting_view,
        'methods': ['GET', ]
    },
    {
        'uri': 'meeting/synchronize',
        'view': synchronize_meeting_view,
        'methods': ['PATCH', ]
    },
    {
        'uri': 'meeting/periodic/patch',
        'view': periodic_auth_view,
        'methods': ['PATCH', ]
    },
    {
        'uri': 'meeting/periodic/delete',
        'view': periodic_auth_view,
        'methods': ['DELETE', ]
    },
    {
        'uri': 'meeting/approval_log',
        'view': approval_log_view,
        'methods': ['GET', ]
    },
    {
        'uri': 'meeting/search',
        'view': meeting_search_view,
        'methods': ['GET', ]
    },

]

meeting_routes.extend(admin_meeting_routes)
