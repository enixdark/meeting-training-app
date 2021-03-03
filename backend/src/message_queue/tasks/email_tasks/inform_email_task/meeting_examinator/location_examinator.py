from . import MeetingExaminator


class LocationExaminator(MeetingExaminator):
    def state_message(self, old_location: str, new_location: str) -> str:
        if self.__compare_location(old_location, new_location):
            return '- Địa điểm được chuyển từ {old_location} sang {new_location}.'.format(
                old_location=old_location,
                new_location=new_location
            )
        return ''

    @staticmethod
    def __compare_location(old_location: str, new_location: str) -> bool:
        return old_location != new_location
