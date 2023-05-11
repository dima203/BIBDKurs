from database_view import BaseRecord, BaseDataBaseView, TaskList, WorksCatalog, CustomerList, SpecificationList

from dataclasses import dataclass, field
from datetime import date


@dataclass()
class ReportContract(BaseRecord):
    contractCode: str = ''
    customerCode: str = ''
    customerLocation: str = ''
    workCode: list[str] = field(default_factory=list)
    workPrice: list[float] = field(default_factory=list)
    taskDate: list[str] = field(default_factory=list)


class ContractReport(BaseDataBaseView):
    def __init__(self, task_view: TaskList, specification_view: SpecificationList,
                 work_view: WorksCatalog, customer_view: CustomerList, debug: bool = False) -> None:
        super().__init__(debug)
        self.table_name = 'Список клиентов СПТ'
        self.id_name = 'customerCode'
        self.fields = ('customerCode', 'contractNumber', 'contractPrice')
        self.record_type = ReportContract
        self.task_view = task_view
        self.specification_view = specification_view
        self.work_view = work_view
        self.customer_view = customer_view

    def get(self, record_id: str) -> BaseRecord:
        pass

    def add(self, record: BaseRecord) -> None:
        pass

    def update(self, record_id: str, record: BaseRecord) -> None:
        pass

    def delete(self, record_id: str) -> None:
        pass

    def get_table(self) -> list[ReportContract]:
        today = date.today()
        contracts = {}
        for task in self.task_view.get_table():
            d = date.fromisoformat('-'.join(reversed(task.taskDate.split('.'))))
            if d.year == today.year and d.month == today.month:
                if task.contractCode not in contracts:
                    contracts[task.contractCode] = []
                contracts[task.contractCode].append(task)

        specifications = self.specification_view.get_table()

        result = []
        for contract, tasks in contracts.items():
            customer_code = None
            for specification in specifications:
                if specification.contractCode == contract:
                    customer_code = specification.customerCode
                    break
            report = ReportContract(contract, customer_code, self.customer_view.get(customer_code).customerLocation)
            for task in tasks:
                for work_code in task.workCode:
                    report.workCode.append(work_code)
                    report.workPrice.append(self.work_view.get(work_code).workPrice)
                    report.taskDate.append(task.taskDate)
            result.append(report)

        return result
