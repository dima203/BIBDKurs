from database_view import BaseRecord, BaseDataBaseView

from dataclasses import dataclass


@dataclass()
class SPT(BaseRecord):
    sptCode: str
    sptName: str
    sptIzm: str
    sptPrice: int

    def to_dict(self) -> dict:
        return {
            'sptCode': self.sptCode,
            'sptName': self.sptName,
            'sptIzm': self.sptIzm,
            'sptPrice': self.sptPrice
        }


class SPTList(BaseDataBaseView):
    def __init__(self, debug: bool = False) -> None:
        super().__init__(debug)
        self.table_name = 'Справочник СПТ'
        self.id_name = 'sptCode'
        self.fields = ('sptCode', 'sptName', 'sptIzm', 'sptPrice')
        self.record_type = SPT
