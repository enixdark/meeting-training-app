from datetime import datetime, timedelta

from config import BaseApiConfig
from src.api.pool.services import FormService
from src.database.postgres.meeting import Meeting


class MeetingTimeService(FormService):
    _NOW = datetime.now() + timedelta(hours=BaseApiConfig.TIME_DIFFERENCE)

    def _create_class_model(self):
        return Meeting
