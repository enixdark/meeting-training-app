from abc import ABC, abstractmethod

from src.api.pool.decorators.meeting_decorators import MeetingAuthDecorator


class BaseApprovalUpdateDecorator(MeetingAuthDecorator, ABC):
    def update_model(self, *args, **kwargs) -> bool:
        approval_kwargs = self._set_approval_state(_id=kwargs['_id'])
        # approval_kwargs['_id'] = kwargs['_id']

        updated = super(BaseApprovalUpdateDecorator, self).update_model(*args, **approval_kwargs)
        return updated

    @abstractmethod
    def _set_approval_state(self, **kwargs) -> dict:
        """
        Set related approval data field, include: state, is_approval
        :return:
        """
        pass
