from src.api.pool.resources.entities.requests.base_requests.schemas.get_schema import GetSchema


class AttendeeLogSchema(GetSchema):
    @staticmethod
    def sort_rule() -> list:
        return ['id', 'started_time', 'finished_time', 'created_at', 'updated_at']

    @staticmethod
    def relation_rule() -> list:
        return []
