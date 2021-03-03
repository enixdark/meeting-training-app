from src.api.pool.resources.entities.requests.implement_requests.meeting_requests import MeetingPatchSchema


class MeetingPeriodicPatchSchema(MeetingPatchSchema):
    def _create_required_attributes(self) -> list:
        return [
            *super(MeetingPeriodicPatchSchema, self)._create_required_attributes()
        ]
