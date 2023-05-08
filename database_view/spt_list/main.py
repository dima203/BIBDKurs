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

    def get(self, spt_id: str) -> SPT:
        return SPT(*self._database.get_record(self.table_name, self.id_name, spt_id)[0])

    def add(self, spt: SPT) -> None:
        self._database.add_record(self.table_name, spt.to_dict())
        self._database.commit()

    def delete(self, spt_id: str) -> None:
        self._database.delete_record(self.table_name, self.id_name, spt_id)
        self._database.commit()

    def update(self, spt_id: str, spt: SPT) -> None:
        self._database.update_record(self.table_name, self.id_name, spt_id, spt.to_dict())
        self._database.commit()

    def get_table(self) -> list[SPT]:
        return [SPT(*spt) for spt in self._database.get_records_from_table(self.table_name)]
