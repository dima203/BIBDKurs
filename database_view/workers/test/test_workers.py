from pytest import raises

from database_view import Workers, Worker


class TestWorkers:
    def setup_class(self) -> None:
        self.workers = Workers(True)

    def test_get_worker(self) -> None:
        worker = self.workers.get('02024')
        assert isinstance(worker, Worker)
        assert worker.workerCode == '02024'

    def test_add_worker(self) -> None:
        worker = Worker('02027', 'Test Test Test', '313400', '12.05.2022', 'Tut', '66-66-66')
        self.workers.add(worker)
        assert self.workers.get('02027')

    def test_delete_worker(self) -> None:
        self.workers.delete('02024')
        with raises(KeyError):
            assert self.workers.get('02024')

    def test_update_worker(self) -> None:
        worker = Worker('06073', 'Бирюков Зиновий Никитевич', '315700', '25.07.2015',
                        'пер. Заречный, д. 15 кв.79', '32-87-09')
        self.workers.update('06073', worker)
        assert self.workers.get('06073') == worker

    def test_get_table(self) -> None:
        works = self.workers.get_table()
        assert works
        assert isinstance(works[0], Worker)
