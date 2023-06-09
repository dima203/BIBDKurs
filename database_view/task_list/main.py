from database_view import BaseRecord, BaseDataBaseView

from dataclasses import dataclass, asdict, field


@dataclass()
class Task(BaseRecord):
    taskCode: str = ''
    contractCode: str = ''
    taskDate: str = ''
    workCode: list[str] = field(default_factory=list)
    workerCode: list[str] = field(default_factory=list)
    taskCost: int = 0

    def __eq__(self, other: 'Task') -> bool:
        return (self.taskCode == other.taskCode
                and self.contractCode == other.contractCode
                and self.taskDate == other.taskDate
                and sorted(self.workCode) == sorted(other.workCode)
                and sorted(self.workerCode) == sorted(other.workerCode)
                and self.taskCost == other.taskCost)


class TaskList(BaseDataBaseView):
    def __init__(self, debug: bool = False) -> None:
        super().__init__(debug)
        self.table_name = 'Наряд-задание'
        self.id_name = 'taskCode'
        self.fields = ('taskCode', 'contractCode', 'taskDate', 'workCode', 'workerCode', 'taskCost')
        self.record_type = Task

    def get(self, task_id: str) -> Task:
        records = self._database.get_record(self.table_name, self.id_name, task_id)
        work_codes = [record[3] for record in records]
        worker_codes = [record[4] for record in records]
        return Task(*records[0][:3], work_codes, worker_codes, *records[0][5:])

    def add(self, specification: Task) -> None:
        for i in range(len(specification.workCode)):
            _specification = asdict(specification)
            _specification['workCode'] = specification.workCode[i]
            _specification['workerCode'] = specification.workerCode[i]
            self._database.add_record(self.table_name, _specification)
        self._database.commit()

    def update(self, specification_id: str, specification: Task) -> None:
        self.delete(specification_id)
        self.add(specification)

    def get_table(self) -> list[Task]:
        tasks = {}
        for record in self._database.get_records_from_table(self.table_name):
            if record[0] in tasks:
                tasks[record[0]].workCode.append(record[3])
                tasks[record[0]].workerCode.append(record[4])
            else:
                tasks[record[0]] = Task(*record[:3], [record[3]], [record[4]], *record[5:])
        return list(tasks.values())
