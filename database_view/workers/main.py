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
        self.record_type = Worker
