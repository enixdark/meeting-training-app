from datetime import datetime

from src.api.pool.services.location_services import LocationFormService
from src.message_queue.tasks.email_tasks.email_factory.email_templates.template_renderer.inform_renderer import \
    InformTemplateRenderer
from src.message_queue.tasks.email_tasks.html_email_task import HTMLEmailTask
from src.message_queue.tasks.email_tasks.inform_email_task.meeting_examinator.location_examinator import \
    LocationExaminator
from src.message_queue.tasks.email_tasks.inform_email_task.meeting_examinator.time_examinator import \
    TimeExaminator
from src.message_queue.tasks.email_tasks.inform_email_task.meeting_examinator.title_examinator import \
    TitleExaminator


class InformEmailTask(HTMLEmailTask):
    CONFIRM_EMAIL_SUBJECT = 'Thông báo đổi lịch!!!'
    old_meeting_title = None
    old_started_time = None
    old_location_id = None
    is_updated = False

    def _create_email_subject(self) -> str:
        return self.CONFIRM_EMAIL_SUBJECT

    def _addition_init(self, *args, **kwargs):
        self.old_meeting_title = kwargs.get('old_meeting_title', None)
        self.old_started_time = kwargs.get('old_started_time', None)
        self.old_location_id = kwargs.get('old_location_id', None)

    def _send_mail(self, mail: dict):
        if self.is_updated:
            super(InformEmailTask, self)._send_mail(**mail)

    def _create_text_body(self) -> str:
        return ''

    def _create_html_body(self) -> str:
        meeting = self._get_meeting()
        meeting_dict = self._retrieve_meeting_information()
        meeting_name = meeting_dict['name']
        location = meeting_dict['location']

        name_str = TitleExaminator().state_message(
            old_title=self.old_meeting_title,
            new_title=meeting_name)
        time_str = TimeExaminator().state_message(
            old_stated_time=datetime.strptime(self.old_started_time, '%Y-%m-%dT%H:%M:%S'),
            new_stated_time=meeting.started_time)
        location_str = LocationExaminator().state_message(
            old_location=self.__create_location_name(self.old_location_id),
            new_location=self.__create_location_name(location['id']))
        content = ''
        if len(name_str) > 0 or len(time_str) > 0 or len(location_str) > 0:
            self.is_updated = True
            content = '''
                    <p style="text-align: center;">Chào bạn.</p>

                    <p style="text-align: center;">Lịch họp về {old_title} mà bạn được mời tham dự có sự thay đổi về nội dung như sau:</p>
                    <ul>
                    '''.format(old_title=self.old_meeting_title)
            if name_str:
                content += '<li>' + name_str
            if time_str:
                content += '<li>' + time_str
            if location_str:
                content += '<li>' + location_str
            content += '''</ul>
                    <br/>
                    <p style="text-align: center;">Vui lòng truy cập ứng dụng vMeeting để xem chi tiết lịch họp.</p>
                    '''

        renderer = InformTemplateRenderer()
        rendered_html = renderer.render(name=self._create_email_subject(), content=content)
        return rendered_html

    def _retrieve_meeting_information(self) -> dict:
        meeting = self._get_meeting()
        return meeting.serialize(inclusion_rs=['location'])

    def __create_location_name(self, location_id: int) -> str:
        location = self._prepared_service(base_service=LocationFormService()).get_model(_id=location_id)
        location = location.serialize()
        return '{name} - {address}'.format(name=location['name'],
                                           address=location['address'])
