from abc import abstractmethod

from config import BaseApiConfig
from src.message_queue.tasks.email_tasks.base_email_task import BaseEmailTask
from src.message_queue.tasks.email_tasks.email_factory.html_mail_sender import HTMLMailSender, MailSender


class HTMLEmailTask(BaseEmailTask):
    def _create_email(self) -> dict:
        return {
            **super(HTMLEmailTask, self)._create_email(),
            'html_body': self._create_html_body(),
            'img_src': self._create_img_src()
        }

    @staticmethod
    def _create_html_body() -> str:
        return ''

    @staticmethod
    def _create_img_src() -> list:
        src = 'src/message_queue/tasks/email_tasks/email_factory/email_templates/template_images/inform_template/'
        return [
            src + 'Btm.png',
            src + 'Collaborate.png',
            src + 'facebook@2x.png',
            src + 'Icon_logo_animate.gif',
            src + 'instagram@2x.png',
            src + 'linkedin@2x.png',
            src + 'twitter@2x.png',
        ]

    @staticmethod
    def _create_mail_sender() -> MailSender:
        return HTMLMailSender(**BaseApiConfig.EMAIL_CONFIG)