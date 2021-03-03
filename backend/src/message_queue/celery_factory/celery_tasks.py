from ..tasks.cell_task import CellTask
from ..tasks.email_tasks import email_tasks
from ..tasks.calendar_tasks import calendar_tasks


celery_tasks = [
    CellTask(),
    *email_tasks,
    *calendar_tasks,

]
