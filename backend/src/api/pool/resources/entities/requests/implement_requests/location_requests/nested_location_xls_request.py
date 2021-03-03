from datetime import datetime, timedelta

from config import BaseApiConfig
from ...base_requests.schema_requests.base_nested_requests import NestedPostRequest
from src.api.pool.resources.entities.requests.base_requests.schemas.nested_schemas import NestedSchema
from .location_schemas.location_xls_schema import NestedLocationXLSSchema


class NestedLocationXLSRequest(NestedPostRequest):
    _NOW = datetime.now() + timedelta(hours=BaseApiConfig.TIME_DIFFERENCE)

    def _create_schema(self) -> NestedSchema:
        return NestedLocationXLSSchema()

    def _get_from_date(self):
        from_date = self._get_url_parameter('ge')
        if from_date:
            return from_date
        else:
            return str(self._NOW.date() - timedelta(days=7))

    def _get_to_date(self):
        to_date = self._get_url_parameter('le')
        if to_date:
            return to_date
        else:
            return str(self._NOW.date() + timedelta(days=7))

    def _get_raw_data(self) -> dict:
        return {
            **super(NestedLocationXLSRequest, self)._get_raw_data(),
            'from_date': self._get_from_date(),
            'to_date': self._get_to_date()
        }
