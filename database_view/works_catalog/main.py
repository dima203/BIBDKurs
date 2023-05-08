from database_view import BaseRecord, BaseDataBaseView

from dataclasses import dataclass


@dataclass()
class Work(BaseRecord):
    workCode: str
    workPrice: int
    workTime: float

    def to_dict(self) -> dict:
        return {
            'workCode': self.workCode,
            'workPrice': self.workPrice,
            'workTime': self.workTime
        }


class WorksCatalog(BaseDataBaseView):
    def __init__(self, debug: bool = False) -> None:
        super().__init__(debug)
        self.table_name = 'Каталог работ'
        self.id_name = 'workCode'
        self.fields = ('workCode', 'workPrice', 'workTime')
        self.record_type = Work
