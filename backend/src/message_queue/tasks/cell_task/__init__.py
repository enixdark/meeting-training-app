from .. import Task


class CellTask(Task):
    def run(self, *args, **kwargs):
        print('cell')
