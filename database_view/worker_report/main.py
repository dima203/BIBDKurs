from database_view import BaseRecord, BaseDataBaseView, TaskList, WorksCatalog, Workers

from dataclasses import dataclass
from datetime import date


@dataclass()
class ReportWorker(BaseRecord):
    workerCode: str = ''
    workerFIO: str = ''
    taskNumber: int = 0
    workPrice: float = 0


class WorkerReport(BaseDataBaseView):
    def __init__(self, worker_view: Workers, task_view: TaskList, work_view: WorksCatalog, debug: bool = False) -> None:
        super().__init__(debug)
        self.table_name = 'Список клиентов СПТ'
        self.id_name = 'customerCode'
        self.fields = ('customerCode', 'contractNumber', 'contractPrice')
        self.record_type = ReportWorker
        self.worker_view = worker_view
        self.task_view = task_view
        self.work_view = work_view

    def get(self, record_id: str) -> BaseRecord:
        pass

    def add(self, record: BaseRecord) -> None:
        pass

    def update(self, record_id: str, record: BaseRecord) -> None:
        pass

    def delete(self, record_id: str) -> None:
        pass

    def get_table(self) -> list[ReportWorker]:
        today = date.today()
        tasks = []
        for task in self.task_view.get_table():
            d = date.fromisoformat('-'.join(reversed(task.taskDate.split('.'))))
            if d.year == today.year and d.month == today.month:
                tasks.append(task)

        workers = {}
        result = []
        for task in tasks:
            for i, workerCode in enumerate(task.workerCode):
                if workerCode not in workers:
                    workers[workerCode] = {'tasks': set(), 'works': []}
                workers[workerCode]['tasks'].add(task.taskCode)
                workers[workerCode]['works'].append(task.workCode[i])

        for workerCode in workers:
            result.append(ReportWorker(workerCode, self.worker_view.get(workerCode).workerFIO,
                                       len(workers[workerCode]['tasks']), sum(self.work_view.get(workCode).workPrice
                                                                            for workCode in
                                                                            workers[workerCode]['works'])))

        return result
