from pytest import raises

from database_view import SPTList, SPT


class TestSPTList:
    def setup_class(self) -> None:
        self.spt_list = SPTList(True)

    def test_get_spt(self) -> None:
        spt = self.spt_list.get('002006389')
        assert isinstance(spt, SPT)
        assert spt.sptCode == '002006389'

    def test_add_spt(self) -> None:
        spt = SPT('002008389', 'TestSPT', 'шт', 50)
        self.spt_list.add(spt)
        assert self.spt_list.get('002008389')

    def test_delete_spt(self) -> None:
        self.spt_list.delete('002035784')
        with raises(KeyError):
            assert self.spt_list.get('002035784')

    def test_update_spt(self) -> None:
        spt = SPT('002006389', 'Test', 'шт', 57)
        self.spt_list.update('002006389', spt)
        assert self.spt_list.get('002006389') == spt

    def test_get_table(self) -> None:
        spt = self.spt_list.get_table()
        assert spt
        assert isinstance(spt[0], SPT)
