from database_view import BaseRecord, BaseDataBaseView

from dataclasses import dataclass


@dataclass()
class Worker(BaseRecord):
    workerCode: str
    workerFIO: str
    professionCode: str
    hireDate: str
    workerLocation: str
    workerPhone: str

    def to_dict(self) -> dict:
        return {
            'workerCode': self.workerCode,
            'workerFIO': self.workerFIO,
            'professionCode': self.professionCode,
            'hireDate': self.hireDate,
            'workerLocation': self.workerLocation,
            'workerPhone': self.workerPhone
        }


class Workers(BaseDataBaseView):
    def __init__(self, debug: bool = False) -> None:
        super().__init__(debug)
        self.table_name = 'Справочник работников цеха'
        self.id_name = 'workerCode'
        self.fields = ('workerCode', 'workerFIO', 'professionCode', 'hireDate', 'workerLocation', 'workerPhone')

    def get(self, worker_id: str) -> Worker:
        return Worker(*self._database.get_record(self.table_name, self.id_name, worker_id)[0])

    def add(self, worker: Worker) -> None:
        self._database.add_record(self.table_name, worker.to_dict())
        self._database.commit()

    def delete(self, worker_id: str) -> None:
        self._database.delete_record(self.table_name, self.id_name, worker_id)
        self._database.commit()

    def update(self, worker_id: str, worker: Worker) -> None:
        self._database.update_record(self.table_name, self.id_name, worker_id, worker.to_dict())
        self._database.commit()

    def get_table(self) -> list[Worker]:
        return [Worker(*worker) for worker in self._database.get_records_from_table(self.table_name)]
