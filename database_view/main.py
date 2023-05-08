from abc import ABC, abstractmethod
from dataclasses import dataclass

from database import DataBase


@dataclass()
class BaseRecord(ABC):
    @abstractmethod
    def to_dict(self) -> dict: ...


class BaseDataBaseView(ABC):
    table_name: str
    id_name: str
    fields: tuple
    record_type: type[BaseRecord]

    def __init__(self, debug: bool = False) -> None:
        self._database = DataBase(debug)

    def get(self, record_id: str) -> BaseRecord:
        return self.record_type(*self._database.get_record(self.table_name, self.id_name, record_id)[0])

    def add(self, record: BaseRecord) -> None:
        self._database.add_record(self.table_name, record.to_dict())
        self._database.commit()

    def delete(self, record_id: str) -> None:
        self._database.delete_record(self.table_name, self.id_name, record_id)
        self._database.commit()

    def update(self, record_id: str, record: BaseRecord) -> None:
        self._database.update_record(self.table_name, self.id_name, record_id, record.to_dict())
        self._database.commit()

    def get_table(self) -> list[BaseRecord]:
        return [self.record_type(*customer) for customer in self._database.get_records_from_table(self.table_name)]
