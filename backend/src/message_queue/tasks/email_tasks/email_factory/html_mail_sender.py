from src.message_queue.tasks.email_tasks.email_factory import MailSender, BaseApiConfig
from .custom_envelope.advanced_envelopes import AdvancedEnvelope, Envelope


class HTMLMailSender(MailSender):
    def _create_envelope(self, to_addr, subject, text_body, html_body: str = None, *args, **kwargs) -> Envelope:
        return AdvancedEnvelope(from_addr=self.account,
                                to_addr=to_addr,
                                subject=subject,
                                text_body=text_body,
                                html_body=html_body)

    def _attach_file(self, envelope: Envelope, *args, **kwargs):
        super(HTMLMailSender, self)._attach_file(envelope, *args, **kwargs)
        if isinstance(envelope, AdvancedEnvelope):
            img_src = kwargs.get('img_src', [])
            if isinstance(img_src, list):
                for src in img_src:
                    envelope.add_src_image(src)

