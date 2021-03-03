import mimetypes
import os
from email import encoders as email_encoders
from email.mime.base import MIMEBase

from envelopes import Envelope


class AdvancedEnvelope(Envelope):
    def add_src_image(self, file_path, mimetype=None, src_name=None):
        """Attaches a file located at *file_path* to the envelope. If
               *mimetype* is not specified an attempt to guess it is made. If nothing
               is guessed then `application/octet-stream` is used."""
        if not mimetype:
            mimetype, _ = mimetypes.guess_type(file_path)

        if mimetype is None:
            mimetype = 'application/octet-stream'

        type_maj, type_min = mimetype.split('/')
        with open(file_path, 'rb') as fh:
            part_data = fh.read()

            part = MIMEBase(type_maj, type_min)
            part.set_payload(part_data)
            email_encoders.encode_base64(part)

            if not src_name:
                part_filename = os.path.basename(self._encoded(file_path))
                src_name = part_filename
            part.add_header('Content-ID', '<{}>'.format(src_name))
            self._parts.append((mimetype, part))
