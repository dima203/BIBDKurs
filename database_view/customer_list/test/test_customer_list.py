from pytest import raises

from database_view import CustomerList, Customer


class TestCustomerList:
    def setup_class(self) -> None:
        self.customer_list = CustomerList(True)

    def test_get_customer(self) -> None:
        customer = self.customer_list.get('020651')
        assert isinstance(customer, Customer)
        assert customer.customerCode == '020651'

    def test_add_customer(self) -> None:
        spt = Customer('020657', 'TestSPT', 'шт', 50)
        self.customer_list.add(spt)
        assert self.customer_list.get('020657')

    def test_delete_customer(self) -> None:
        self.customer_list.delete('020651')
        with raises(KeyError):
            assert self.customer_list.get('020651')

    def test_update_customer(self) -> None:
        customer = Customer('031832', 'Test T. T.', 'ул. Железнодорожная, д. 21 кв.19', '64-94-43')
        self.customer_list.update('031832', customer)
        assert self.customer_list.get('031832') == customer

    def test_get_table(self) -> None:
        customer = self.customer_list.get_table()
        assert customer
        assert isinstance(customer[0], Customer)
