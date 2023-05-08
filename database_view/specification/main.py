from database_view import BaseRecord, BaseDataBaseView

from dataclasses import dataclass


@dataclass()
class Specification(BaseRecord):
    specificationCode: str
    contractCode: str
    customerCode: str
    sptCode: str
    workCodes: list[str]
    cost: int

    def to_dict(self) -> dict:
        return {
            'specificationCode': self.specificationCode,
            'contractCode': self.contractCode,
            'customerCode': self.customerCode,
            'sptCode': self.sptCode,
            'workCode': self.workCodes,
            'cost': self.cost
        }

    def __eq__(self, other: 'Specification') -> bool:
        return (self.specificationCode == other.specificationCode
                and self.contractCode == other.contractCode
                and self.customerCode == other.customerCode
                and self.sptCode == other.sptCode
                and sorted(self.workCodes) == sorted(other.workCodes)
                and self.cost == other.cost)


class SpecificationList(BaseDataBaseView):
    def __init__(self, debug: bool = False) -> None:
        super().__init__(debug)
        self.table_name = 'Спецификация на выполнение работ'
        self.id_name = 'specificationCode'
        self.fields = ('specificationCode', 'contractCode', 'customerCode', 'sptCode', 'workCode', 'cost')

    def get(self, specification_id: str) -> Specification:
        records = self._database.get_record(self.table_name, self.id_name, specification_id)
        work_codes = [record[4] for record in records]

        return Specification(*records[0][:4], work_codes, *records[0][5:])

    def add(self, specification: Specification) -> None:
        for work_code in specification.workCodes:
            _specification = specification.to_dict()
            _specification['workCode'] = work_code
            self._database.add_record(self.table_name, _specification)
        self._database.commit()

    def delete(self, specification_id: str) -> None:
        self._database.delete_record(self.table_name, self.id_name, specification_id)
        self._database.commit()

    def update(self, specification_id: str, specification: Specification) -> None:
        self.delete(specification_id)
        self.add(specification)

    def get_table(self) -> list[Specification]:
        return [Specification(*specification) for specification in self._database.get_records_from_table(self.table_name)]
