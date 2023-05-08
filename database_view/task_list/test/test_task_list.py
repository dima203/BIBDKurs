from pytest import raises

from database_view import TaskList, Task


class TestTaskList:
    def setup_class(self) -> None:
        self.task_list = TaskList(True)

    def test_get_task(self) -> None:
        specification = self.task_list.get('1')
        assert isinstance(specification, Task)
        assert specification.taskCode == '1'

    def test_add_task(self) -> None:
        specification = Task('2', '2', '12.12.2012', ['021019'], ['02024'], 29)
        self.task_list.add(specification)
        assert self.task_list.get('2')

    def test_delete_task(self) -> None:
        self.task_list.delete('2')
        with raises(KeyError):
            assert self.task_list.get('2')

    def test_update_task(self) -> None:
        specification = Task('1', '1', '19.08.2018', ['030523'], ['02024'], 14)
        self.task_list.update('1', specification)
        assert self.task_list.get('1') == specification

    def test_get_table(self) -> None:
        specification = self.task_list.get_table()
        assert specification
        assert isinstance(specification[0], Task)
