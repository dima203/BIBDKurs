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

    def __init__(self, debug: bool = False) -> None:
        self._database = DataBase(debug)

    @abstractmethod
    def get(self, record_id: str) -> BaseRecord: ...

    @abstractmethod
    def add(self, record: BaseRecord) -> None: ...

    @abstractmethod
    def delete(self, record_id: str) -> None: ...

    @abstractmethod
    def update(self, record_id: str, record: BaseRecord) -> None: ...

    @abstractmethod
    def get_table(self) -> list[BaseRecord]: ...
