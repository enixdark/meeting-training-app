from . import MeetingExaminator


class TitleExaminator(MeetingExaminator):
    def state_message(self, old_title: str, new_title: str) -> str:
        if self.__compare_title(old_title, new_title):
            return '- Nội dung cũ: {old_title} được chuyển sang nội dung mới {new_title}.'.format(
                old_title=old_title,
                new_title=new_title
            )
        return ''

    @staticmethod
    def __compare_title(old_title: str, new_title: str) -> bool:
        return old_title != new_title
