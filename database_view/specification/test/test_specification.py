from pytest import raises

from database_view import SpecificationList, Specification


class TestSpecificationList:
    def setup_class(self) -> None:
        self.specification_list = SpecificationList(True)

    def test_get_customer(self) -> None:
        specification = self.specification_list.get('1')
        assert isinstance(specification, Specification)
        assert specification.specificationCode == '1'

    def test_add_customer(self) -> None:
        specification = Specification('2', '2', '020651', '002006389', ['030523'], 14)
        self.specification_list.add(specification)
        assert self.specification_list.get('2')

    def test_delete_customer(self) -> None:
        self.specification_list.delete('020651')
        with raises(KeyError):
            assert self.specification_list.get('020651')

    def test_update_customer(self) -> None:
        specification = Specification('1', '1', '020651', '002006389', ['030523', '021019'], 43)
        self.specification_list.update('1', specification)
        assert self.specification_list.get('1') == specification

    def test_get_table(self) -> None:
        specification = self.specification_list.get_table()
        assert specification
        assert isinstance(specification[0], Specification)
