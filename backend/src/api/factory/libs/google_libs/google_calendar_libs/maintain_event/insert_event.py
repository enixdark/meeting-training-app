import json

import requests

from . import MaintainEventExecutor


class InsertEventExecutor(MaintainEventExecutor):
    def _create_action_endpoint(self) -> str:
        return self._calendar_id + '/events/'

    def _send_request(self, meeting_data: dict, access_token: str) -> dict:
        response = requests.post(**self._build_maintained_request(meeting_data=meeting_data, access_token=access_token))
        return json.loads(response.content.decode())
