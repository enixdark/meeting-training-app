from src.message_queue.tasks.email_tasks.email_factory.email_templates.template_renderer.inform_renderer import \
    InformTemplateRenderer
from . import BaseRetrieveMeetingEmailTask


class ConfirmEmailTask(BaseRetrieveMeetingEmailTask):
    CONFIRM_EMAIL_SUBJECT = 'Thư xác nhận!!!'
    confirm_name = ''
    confirm_email = ''
    confirm_status = ''

    def _create_email_subject(self) -> str:
        return self.CONFIRM_EMAIL_SUBJECT

    def _addition_init(self, *args, **kwargs):
        self.confirm_name = kwargs.get('confirm_name', 'name')
        self.confirm_email = kwargs.get('confirm_email', 'email')
        self.confirm_status = kwargs.get('confirm_status', 'status')

    def _create_text_body(self) -> str:
        return ''

    def _create_html_body(self) -> str:
        meeting_dict = self._retrieve_meeting_information()
        location = meeting_dict['location']
        location_name = '{name} - {address}'.format(name=location['name'],
                                                    address=location['address'])

        content = \
            '''
            <p style="text-align: center;">Thành viên {name}|{email} đã
            <strong>{confirm}</strong> tham dự cuộc họp có nội dung 
            <br /><strong>{title}</strong> do bạn tổ chức vào lúc:
            {time} tại {location}>.
            <br /><br />
            Vui lòng truy cập ứng dụng vMeeting để xem chi tiết.</p>
                    '''.format(name=self.confirm_name,
                               email=self.confirm_email,
                               confirm=self.confirm_status,
                               title=meeting_dict['name'],
                               time=self._create_meeting_time(),
                               location=location_name)
        email_name = '{name} đã {confirm}'.format(name=self.confirm_name, confirm=self.confirm_status)
        renderer = InformTemplateRenderer()
        rendered_html = renderer.render(name=email_name, content=content)
        return rendered_html
