from src.message_queue.tasks.email_tasks.email_factory.email_templates.template_renderer.inform_renderer import \
    InformTemplateRenderer
from . import BaseRetrieveMeetingEmailTask


class ApprovalEmailTask(BaseRetrieveMeetingEmailTask):
    APPROVAL_EMAIL_SUBJECT = 'Thông báo chấp thuận yêu cầu.'

    def _create_email_subject(self) -> str:
        return self.APPROVAL_EMAIL_SUBJECT

    def _create_text_body(self) -> str:
        return ''

    def _create_html_body(self) -> str:
        meeting = self._get_meeting()
        approval_str = 'được chấp thuận'
        content = '''
                <p style="text-align: center;">Yêu cầu tạo buổi họp</p>
                <p style="text-align: center;"><strong>{title}</strong></p>
                <p style="text-align: center;">vào lúc: {time},</p>
                <p style="text-align: center;">tại {location}</p>
                <p style="text-align: center;">{approval_state} bởi người quản lý phòng họp.<br /></p>
                <p style="text-align: center;"><br /> 
                Vui lòng truy cập ứng dụng vMeeting để xác nhận lịch.
                </p>
                
                '''.format(title=meeting.name,
                           time=self._create_meeting_time(),
                           location=self._create_meeting_location(),
                           approval_state=approval_str)
        renderer = InformTemplateRenderer()
        rendered_html = renderer.render(name='Yêu cầu đã được chấp thuận', content=content)
        return rendered_html
