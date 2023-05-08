from pytest import raises

from database import DataBase


class TestDataBase:
    def setup_method(self) -> None:
        self.database = DataBase(True)

    def test_get_table(self) -> None:
        assert self.database.get_records_from_table("Каталог работ") == [('021019', 29, 2.5), ('030523', 14, 1)]

    def test_get_record(self) -> None:
        assert self.database.get_record("Каталог работ", 'workCode', '021019')

    def test_get_wrong_record(self) -> None:
        with raises(KeyError):
            self.database.get_record("Каталог работ", 'workCode', '1')

    def test_update_record(self) -> None:
        record = self.database.get_record("Каталог работ", 'workCode', '021019')
        record_dict = dict(workCode=record[0], workPrice=record[1], workTime=record[2])
        record_dict['workPrice'] = 27
        self.database.update_record("Каталог работ", 'workCode', '021019', record_dict)
        self.database.commit()
        assert self.database.get_record("Каталог работ", 'workCode', '021019') == list(record_dict.values())

    def test_add_record(self) -> None:
        record = {
            'workCode': '010101',
            'workPrice': 1,
            'workTime': 1
        }
        self.database.add_record("Каталог работ", record)
        self.database.commit()
        assert self.database.get_record("Каталог работ", 'workCode', record['workCode'])

    def test_delete_record(self) -> None:
        self.database.delete_record("Каталог работ", 'workCode', '021019')
        self.database.commit()
        with raises(KeyError):
            self.database.get_record("Каталог работ", 'workCode', '021019')
