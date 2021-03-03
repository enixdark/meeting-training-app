from src.message_queue.tasks.email_tasks.email_factory.email_templates.template_renderer.inform_renderer import \
    InformTemplateRenderer
from src.message_queue.tasks.email_tasks.retrieve_meeting_email_task import BaseRetrieveMeetingEmailTask


class CancelEmailTask(BaseRetrieveMeetingEmailTask):
    __CANCEL_EMAIL_SUBJECT = 'Hủy cuộc họp'

    def _create_email_subject(self) -> str:
        return self.__CANCEL_EMAIL_SUBJECT

    def _create_text_body(self) -> str:
        return ''

    def _create_html_body(self) -> str:
        meeting_dict = self._retrieve_meeting_information()
        content = \
            '''
            <p style="text-align: center;">Cuộc họp <strong>{title}</strong></p>
            <p style="text-align: center;">vào lúc: {time},</p>
            <p style="text-align: center;">tại {location} mà bạn xác nhận tham gia đã bị hủy.</p>
            <p style="text-align: center;"><br /> Vui lòng truy cập ứng dụng vMeeting để xem thêm chi tiết.</p>
            '''.format(title=meeting_dict['name'],
                       time=self._create_meeting_time(),
                       location=self._create_meeting_location()
                       )
        renderer = InformTemplateRenderer()
        rendered_html = renderer.render(name='Buổi họp đã bị hủy', content=content)
        return rendered_html
