from src.message_queue.tasks.email_tasks.email_factory.email_templates.template_renderer.inform_renderer import \
    InformTemplateRenderer
from . import BaseRetrieveMeetingEmailTask


class RequestApprovalEmailTask(BaseRetrieveMeetingEmailTask):
    REQUEST_APPROVAL_SUBJECT = 'Yêu cầu duyệt tạo lịch họp.'

    def _create_email_subject(self) -> str:
        return self.REQUEST_APPROVAL_SUBJECT

    def _create_text_body(self) -> str:
        return ''

    def _create_html_body(self) -> str:
        meeting = self._get_meeting()
        content = """
        <p style="text-align: center;">Bạn được yêu cầu duyệt cuộc họp với nội dung:</p>
        <p style="text-align: center;"><strong>{title}</strong></p>
        <p style="text-align: center;">vào lúc: {time},</p>
        <p style="text-align: center;">Tại {location},</p>
        <p style="text-align: center;">với nội dung:</p>
        <p style="text-align: center;">{description}.</p><br />
        <p style="text-align: center;">Vui lòng truy cập ứng dụng vMeeting để xem chi tiết.</p>
        """.format(title=meeting.name,
                   time=self._create_meeting_time(),
                   location=self._create_meeting_location(),
                   description=meeting.description
                   )
        renderer = InformTemplateRenderer()
        rendered_html = renderer.render(name=self._create_email_subject(), content=content)
        return rendered_html
