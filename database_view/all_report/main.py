from database_view import BaseRecord, BaseDataBaseView, TaskList, SpecificationList

from dataclasses import dataclass
from datetime import date


@dataclass()
class ReportAll(BaseRecord):
    allContractNumber: int = 0
    completeContractNumber: int = 0
    sptNumber: int = 0
    workPrice: float = 0


class AllReport(BaseDataBaseView):
    def __init__(self, task_view: TaskList, specification_view: SpecificationList, debug: bool = False) -> None:
        super().__init__(debug)
        self.table_name = 'Список клиентов СПТ'
        self.id_name = 'customerCode'
        self.fields = ('customerCode', 'contractNumber', 'contractPrice')
        self.record_type = ReportAll
        self.task_view = task_view
        self.specification_view = specification_view

    def get(self, record_id: str) -> BaseRecord:
        pass

    def add(self, record: BaseRecord) -> None:
        pass

    def update(self, record_id: str, record: BaseRecord) -> None:
        pass

    def delete(self, record_id: str) -> None:
        pass

    def get_table(self) -> list[ReportAll]:
        today = date.today()
        tasks = []
        for task in self.task_view.get_table():
            d = date.fromisoformat('-'.join(reversed(task.taskDate.split('.'))))
            if d.year == today.year:
                tasks.append(task)

        spts = set()
        for specification in self.specification_view.get_table():
            if specification.contractCode in [task.contractCode for task in tasks]:
                spts.add(specification.sptCode)

        return [
            ReportAll(len(set(task.contractCode for task in tasks)), len(set(task.contractCode for task in tasks)),
                      len(spts), sum(task.taskCost for task in tasks))
        ]
