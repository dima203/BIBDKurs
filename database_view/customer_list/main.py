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
        self.record_type = Customer
