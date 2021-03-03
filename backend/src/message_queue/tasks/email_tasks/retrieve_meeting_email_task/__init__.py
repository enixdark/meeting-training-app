from src.message_queue.tasks.email_tasks.html_email_task import HTMLEmailTask


class BaseRetrieveMeetingEmailTask(HTMLEmailTask):
    def _create_email_subject(self) -> str:
        return ''

    def _create_text_body(self) -> str:
        return ''

    def _create_meeting_time(self) -> str:
        meeting = self._get_meeting()
        return '{stated} đến {finished}, ngày {date}'.format(
            date=meeting.started_time.strftime("%m/%d/%Y"),
            stated=meeting.started_time.strftime("%H:%M:%S"),
            finished=meeting.finished_time.strftime("%H:%M:%S"))

    def _create_meeting_location(self) -> str:
        meeting_dict = self._retrieve_meeting_information()
        location = meeting_dict['location']
        return '{name} - {address}'.format(
            name=location['name'],
            address=location['address'])