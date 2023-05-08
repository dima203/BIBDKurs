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

    def get(self, work_id: str) -> Work:
        return Work(*self._database.get_record(self.table_name, self.id_name, work_id))

    def add(self, work: Work) -> None:
        self._database.add_record(self.table_name, work.to_dict())
        self._database.commit()

    def delete(self, work_id: str) -> None:
        self._database.delete_record(self.table_name, self.id_name, work_id)
        self._database.commit()

    def update(self, work_id: str, work: Work) -> None:
        self._database.update_record(self.table_name, self.id_name, work_id, work.to_dict())
        self._database.commit()

    def get_table(self) -> list[Work]:
        return [Work(*work) for work in self._database.get_records_from_table(self.table_name)]
