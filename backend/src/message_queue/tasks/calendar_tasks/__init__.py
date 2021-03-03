from .create_event_task import CreateEventTask
from src.message_queue.tasks.calendar_tasks.id_base_event_task.delete_event_task import DeleteEventTask
from src.message_queue.tasks.calendar_tasks.id_base_event_task.update_event_task import UpdateEventTask
from src.message_queue.tasks.calendar_tasks.id_base_event_task.confirm_event_task import ConfirmEventTask

calendar_tasks = [
    CreateEventTask(),
    UpdateEventTask(),
    DeleteEventTask(),
    ConfirmEventTask(),
]
