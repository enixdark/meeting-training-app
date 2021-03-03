from envelopes import Envelope, GMailSMTP

from config import BaseApiConfig
from src.api.factory.exceptions.email_exceptions import EmailException


class MailSender(object):

    def __init__(self, account, username, password, smtp, port, **kwargs):

        self.account = account
        self.username = username
        self.password = password
        self.smtp = smtp
        self.port = port

    def send(self, to_addr, subject, text_body, html_body: str = None, gmail=False, *args, **kwargs):
        envelope = self._create_envelope(to_addr, subject, text_body=text_body, html_body=html_body)

        # send attachment
        self._attach_file(envelope, *args, **kwargs)
        return self.__send_mail(envelope, gmail)

    def __send_mail(self, envelope: Envelope, gmail: bool):
        account = self.account
        port = self.port
        smtp = self.smtp
        username = self.username
        password = self.password
        try:
            if not gmail:
                response = envelope.send(smtp, login=username, port=port,
                                         password=password, tls=True)
            else:
                gmail = GMailSMTP(account, password)
                response = gmail.send(envelope)

        except Exception as e:
            raise EmailException(e)
        return response

    @staticmethod
    def _attach_file(envelope: Envelope, *args, **kwargs):
        file_paths = kwargs.get('file_paths', [])
        if isinstance(file_paths, list):
            for file_path in file_paths:
                if isinstance(file_path, dict):
                    path = file_path.get('path', None)
                    mime = file_path.get('mime', None)
                    if path:
                        if not mime:
                            envelope.add_attachment(file_path=path)
                        else:
                            envelope.add_attachment(file_path=path, mimetype=mime)

    def _create_envelope(self, to_addr, subject, text_body, html_body: str = None, *args, **kwargs) -> Envelope:
        return Envelope(from_addr=self.account,
                        to_addr=to_addr,
                        subject=subject,
                        text_body=text_body,
                        html_body=html_body)
