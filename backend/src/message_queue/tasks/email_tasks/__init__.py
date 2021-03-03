from .inform_email_task import InformEmailTask
from .retrieve_meeting_email_task.approval_email_task import ApprovalEmailTask
from .retrieve_meeting_email_task.disapproval_email_task import DisapprovalEmailTask
from .retrieve_meeting_email_task.cancel_email_task import CancelEmailTask
from .retrieve_meeting_email_task.confirm_email_task import ConfirmEmailTask
from .retrieve_meeting_email_task.invited_email_task import InvitedEmailTask
from .retrieve_meeting_email_task.request_approval_email_task import RequestApprovalEmailTask
from .attach_xls_task import AttachXLSTask

email_tasks = [
    ConfirmEmailTask(),
    InvitedEmailTask(),
    InformEmailTask(),
    ApprovalEmailTask(),
    RequestApprovalEmailTask(),
    CancelEmailTask(),
    AttachXLSTask(),
]
