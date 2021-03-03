from src.message_queue.tasks.email_tasks.email_factory.email_templates.template_renderer.inform_renderer import \
    InformTemplateRenderer
from . import BaseRetrieveMeetingEmailTask


class InvitedEmailTask(BaseRetrieveMeetingEmailTask):
    INVITED_EMAIL_SUBJECT = 'Thư mời tham gia!!!'

    def _create_email_subject(self) -> str:
        return self.INVITED_EMAIL_SUBJECT

    def _create_text_body(self) -> str:
        return ''

    def _create_html_body(self) -> str:
        meeting_dict = self._retrieve_meeting_information()
        content = '''
                <p style="text-align: center;">Bạn được mời tham gia vào cuộc họp với nội dung</p>
                <p style="text-align: center;"> <strong>{title}</strong></p>
                <p style="text-align: center;">vào lúc: {time},</p>
                <p style="text-align: center;">tại {location}.</p>
                <p style="text-align: center;"><br /> 
                Vui lòng truy cập ứng dụng vMeeting để xác nhận lịch.
                </p>
                '''.format(title=meeting_dict['name'],
                           time=self._create_meeting_time(),
                           location=self._create_meeting_location()
                           )
        renderer = InformTemplateRenderer()
        rendered_html = renderer.render(name='Bạn được mời tham gia buổi họp', content=content)
        return rendered_html
