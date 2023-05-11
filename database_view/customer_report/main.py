from database_view import BaseRecord, BaseDataBaseView, TaskList, SpecificationList

from dataclasses import dataclass
from datetime import date


@dataclass()
class ReportCustomer(BaseRecord):
    customerCode: str = ''
    contractNumber: int = 0
    contractPrice: float = 0


class CustomerReport(BaseDataBaseView):
    def __init__(self, task_view: TaskList, specification_view: SpecificationList, debug: bool = False) -> None:
        super().__init__(debug)
        self.table_name = 'Список клиентов СПТ'
        self.id_name = 'customerCode'
        self.fields = ('customerCode', 'contractNumber', 'contractPrice')
        self.record_type = ReportCustomer
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

    def get_table(self) -> list[ReportCustomer]:
        today = date.today()
        tasks = []
        for task in self.task_view.get_table():
            d = date.fromisoformat('-'.join(reversed(task.taskDate.split('.'))))
            if d.year == today.year and d.month == today.month:
                tasks.append(task)

        specifications = []
        customers = {}
        for specification in self.specification_view.get_table():
            if specification.contractCode in [task.contractCode for task in tasks]:
                specifications.append(specification)

        for specification in specifications:
            if specification.customerCode not in customers:
                customers[specification.customerCode] = ReportCustomer(specification.customerCode, 1, 0)
            for task in tasks:
                if task.contractCode == specification.contractCode:
                    customers[specification.customerCode].contractPrice += task.taskCost

        return list(customers.values())
