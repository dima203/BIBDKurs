from database_view import BaseRecord, BaseDataBaseView

from dataclasses import dataclass


@dataclass()
class Customer(BaseRecord):
    customerCode: str
    customerName: str
    customerLocation: str
    customerPhone: str

    def to_dict(self) -> dict:
        return {
            'customerCode': self.customerCode,
            'customerName': self.customerName,
            'customerLocation': self.customerLocation,
            'customerPhone': self.customerPhone
        }


class CustomerList(BaseDataBaseView):
    def __init__(self, debug: bool = False) -> None:
        super().__init__(debug)
        self.table_name = 'Список клиентов СПТ'
        self.id_name = 'customerCode'
        self.fields = ('customerCode', 'customerName', 'customerLocation', 'customerPhone')

    def get(self, customer_id: str) -> Customer:
        return Customer(*self._database.get_record(self.table_name, self.id_name, customer_id))

    def add(self, customer: Customer) -> None:
        self._database.add_record(self.table_name, customer.to_dict())
        self._database.commit()

    def delete(self, customer_id: str) -> None:
        self._database.delete_record(self.table_name, self.id_name, customer_id)
        self._database.commit()

    def update(self, customer_id: str, customer: Customer) -> None:
        self._database.update_record(self.table_name, self.id_name, customer_id, customer.to_dict())
        self._database.commit()

    def get_table(self) -> list[Customer]:
        return [Customer(*customer) for customer in self._database.get_records_from_table(self.table_name)]
