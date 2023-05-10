from database_view import BaseRecord, BaseDataBaseView

from dataclasses import dataclass, asdict, field


@dataclass()
class Specification(BaseRecord):
    specificationCode: str = ''
    contractCode: str = ''
    customerCode: str = ''
    sptCode: str = ''
    workCode: list[str] = field(default_factory=list)
    cost: int = 0

    def __eq__(self, other: 'Specification') -> bool:
        return (self.specificationCode == other.specificationCode
                and self.contractCode == other.contractCode
                and self.customerCode == other.customerCode
                and self.sptCode == other.sptCode
                and sorted(self.workCode) == sorted(other.workCode)
                and self.cost == other.cost)


class SpecificationList(BaseDataBaseView):
    def __init__(self, debug: bool = False) -> None:
        super().__init__(debug)
        self.table_name = 'Спецификация на выполнение работ'
        self.id_name = 'specificationCode'
        self.fields = ('specificationCode', 'contractCode', 'customerCode', 'sptCode', 'workCode', 'cost')
        self.record_type = Specification

    def get(self, specification_id: str) -> Specification:
        records = self._database.get_record(self.table_name, self.id_name, specification_id)
        work_codes = [record[4] for record in records]
        return Specification(*records[0][:4], work_codes, *records[0][5:])

    def add(self, specification: Specification) -> None:
        for work_code in specification.workCode:
            _specification = asdict(specification)
            _specification['workCode'] = work_code
            self._database.add_record(self.table_name, _specification)
        self._database.commit()

    def update(self, specification_id: str, specification: Specification) -> None:
        self.delete(specification_id)
        self.add(specification)

    def get_table(self) -> list[Specification]:
        specifications = {}
        for record in self._database.get_records_from_table(self.table_name):
            if record[0] in specifications:
                specifications[record[0]].workCode.append(record[4])
            else:
                specifications[record[0]] = Specification(*record[:4], [record[4]], *record[5:])
        return list(specifications.values())
