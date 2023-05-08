from pytest import raises

from database_view.works_catalog import WorksCatalog, Work


class TestWorksCatalog:
    def setup_class(self) -> None:
        self.works_catalog = WorksCatalog(True)

    def test_get_work(self) -> None:
        work = self.works_catalog.get('021019')
        assert isinstance(work, Work)
        assert work.workCode == '021019' and work.workPrice == 29 and work.workTime == 2.5

    def test_add_work(self) -> None:
        work = Work('010101', 1, 1)
        self.works_catalog.add(work)
        assert self.works_catalog.get('010101')

    def test_delete_work(self) -> None:
        self.works_catalog.delete('021019')
        with raises(KeyError):
            assert self.works_catalog.get('021019')

    def test_update_work(self) -> None:
        work = Work('030523', 17, 1)
        self.works_catalog.update('030523', work)
        assert self.works_catalog.get('030523') == work

    def test_get_table(self) -> None:
        works = self.works_catalog.get_table()
        assert works
        assert isinstance(works[0], Work)
