from .meeting_approval_resource import MeetingApprovalAPI
from .meeting_disapproval_resource import MeetingDisapprovalAPI
from .periodic_meeting_admin_auth_resource import PeriodicMeetingAdminPatchAPI
from .meeting_admin_auth_resource import MeetingAdminPatchAPI

approval_view = MeetingApprovalAPI.as_view('approval_api')
disapproval_view = MeetingDisapprovalAPI.as_view('disapproval_api')
admin_patch_view = MeetingAdminPatchAPI.as_view('admin_patch_view')
periodic_admin_patch_view = PeriodicMeetingAdminPatchAPI.as_view('periodic_admin_patch_view')

admin_meeting_routes = [
    {
        'uri': 'meeting/admin/approve',
        'view': approval_view,
        'methods': ['PATCH', ]
    },
    {
        'uri': 'meeting/admin/disapprove',
        'view': disapproval_view,
        'methods': ['PATCH', 'DELETE']
    },
    {
        'uri': 'meeting/admin/patch',
        'view': admin_patch_view,
        'methods': ['PATCH', ]
    },
    {
        'uri': 'meeting/admin/post',
        'view': admin_patch_view,
        'methods': ['POST', ]
    },
    {
        'uri': 'meeting/admin/periodic/patch',
        'view': periodic_admin_patch_view,
        'methods': ['PATCH', ]
    },
]
