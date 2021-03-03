from src.api.pool.decorators.decorator_helpers.decorator_counters import DecoratorCounter


class UpdateDecoratorCounter(DecoratorCounter):
    def _create_default_success_message(self) -> str:
        return 'Update successfully'

    def _create_default_failed_message(self) -> str:
        return 'Update failed'
