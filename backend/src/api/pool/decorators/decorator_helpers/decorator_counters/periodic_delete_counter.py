from src.api.pool.decorators.decorator_helpers.decorator_counters import DecoratorCounter


class PeriodicDeleteCounter(DecoratorCounter):
    def _create_default_success_message(self) -> str:
        return 'Delete successfully'

    def _create_default_failed_message(self) -> str:
        return 'Delete failed'
