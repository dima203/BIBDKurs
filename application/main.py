from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.expansionpanel import MDExpansionPanelOneLine, MDExpansionPanel
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivy.properties import StringProperty, NumericProperty, ListProperty, ObjectProperty
from kivy.animation import Animation

import hashlib
import datetime
import os
from dataclasses import astuple, asdict

from database_view import CustomerList, Customer, Workers, Worker, WorksCatalog, Work, SPTList, SPT,\
    SpecificationList, Specification, TaskList, Task, BaseDataBaseView, BaseRecord
from database import DataBase


class Menu(MDNavigationDrawer):
    pass


class Navigation(MDTopAppBar):
    pass


class Card(MDCard):
    id = StringProperty('')

    def get_lists(self) -> tuple[list]:
        return ()


class CustomerCard(Card):
    customerCode = StringProperty('')
    customerName = StringProperty('')
    customerLocation = StringProperty('')
    customerPhone = StringProperty('')


class WorkerCard(Card):
    workerCode = StringProperty('')
    workerFIO = StringProperty('')
    professionCode = StringProperty('')
    hireDate = StringProperty('')
    workerLocation = StringProperty('')
    workerPhone = StringProperty('')


class WorkCard(Card):
    workCode = StringProperty('')
    workPrice = NumericProperty(0)
    workTime = NumericProperty(0)


class SPTCard(Card):
    sptCode = StringProperty('')
    sptName = StringProperty('')
    sptIzm = StringProperty('')
    sptPrice = NumericProperty(0)


class SpecificationCard(Card):
    specificationCode = StringProperty('')
    contractCode = StringProperty('')
    customerCode = StringProperty('')
    sptCode = StringProperty('')
    workCode = ListProperty([])
    content = ObjectProperty()
    cost = NumericProperty(0)

    def get_lists(self) -> tuple[list]:
        return self.workCode,


class TaskCard(Card):
    taskCode = StringProperty('')
    contractCode = StringProperty('')
    taskDate = StringProperty('')
    workCode = ListProperty([])
    workerCode = ListProperty([])
    content = ObjectProperty()
    taskCost = NumericProperty(0)

    def get_lists(self) -> tuple[list]:
        return self.workCode, self.workerCode


class AddButton(MDRectangleFlatButton):
    def __init__(self, callback, **kwargs) -> None:
        super().__init__(**kwargs)
        self.callback = callback

    def on_press(self):
        self.callback()


class ListAddButton(MDRectangleFlatButton):
    def __init__(self, callback, card, **kwargs) -> None:
        super().__init__(**kwargs)
        self.callback = callback
        self.card = card

    def on_press(self):
        self.callback(self.card)


class DeleteWorkCodeButton(MDIconButton):
    def __init__(self, callback, card, work_code, **kwargs) -> None:
        super().__init__(**kwargs)
        self.icon = 'trash-can'
        self.theme_icon_color = 'Custom'
        self.icon_color = MDApp.get_running_app().error_color
        self.callback = callback
        self.card = card
        self.work_code = work_code

    def on_press(self):
        self.callback(self.card, self.work_code)


class TableView(MDScrollView):
    database_view: BaseDataBaseView
    record_card_type: type[Card]
    record_type: type[BaseRecord]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.records: list = self.database_view.get_table()
        self.records_list = MDGridLayout(cols=1, spacing=10, size_hint_y=None, padding=20)
        self.records_list.bind(minimum_height=self.records_list.setter('height'))
        self.add_button = AddButton(self.add, text='Добавить')

        for record in self.records:
            self._add_card(record)
        self.records_list.add_widget(self.add_button)

        self.add_widget(self.records_list)

    def add(self) -> None:
        record = self.record_type()
        MDApp.get_running_app().add(self.database_view, record)
        self.records_list.remove_widget(self.add_button)
        self._add_card(record)
        self.records_list.add_widget(self.add_button)

    def _add_card(self, record: BaseRecord) -> None:
        card = self.record_card_type(
            id=f'{astuple(record)[0]}',
            **asdict(record),
            size_hint_y=None,
            height=100
        )
        self.records_list.add_widget(card)


class OperationsTableView(TableView):
    inside_list_cols: int

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def _add_card(self, record: BaseRecord) -> None:
        card = self.record_card_type(
            id=f'{astuple(record)[0]}',
            **asdict(record),
            content=MDGridLayout(
                size_hint_y=None,
                adaptive_height=True,
                cols=self.inside_list_cols + 1,
            ),
            size_hint_y=None,
            height=100
        )
        self.records_list.add_widget(card)

        card.ids.panel_layout.add_widget(MDExpansionPanel(
            icon="plus",
            content=card.content,
            panel_cls=MDExpansionPanelOneLine(
                text="Список работ",
                on_release=(lambda _: self._update_fields(card))
            )
        ))

        self._update_fields(card)

    def _update_fields(self, card: Card):
        card.content.clear_widgets()

        for fields in zip(*[field for field in card.get_lists() if isinstance(field, list)]):
            for field in fields:
                card.content.add_widget(MDTextField(text=field))
            card.content.add_widget(DeleteWorkCodeButton(self._delete_inside_list_record, card, fields[0]))

        card.content.add_widget(ListAddButton(self._add_inside_list_record, card, text='Добавить'))
        if card.ids.panel_layout.children[0].get_state() == 'open':
            animation = Animation(
                height=card.content.height + card.ids.panel_layout.children[0].height,
                d=card.ids.panel_layout.children[0].opening_time,
                t=card.ids.panel_layout.children[0].opening_transition
            )

        else:
            animation = Animation(
                height=100,
                d=card.ids.panel_layout.children[0].closing_time,
                t=card.ids.panel_layout.children[0].closing_transition
            )
        animation.start(card)

    def _add_inside_list_record(self, card: Card):
        for field in card.get_lists():
            field.append('')
        card.ids.panel_layout.children[0].close_panel(card.ids.panel_layout.children[0], True)
        card.ids.panel_layout.children[0].remove_widget(card.content)
        self._update_fields(card)

    def _delete_inside_list_record(self, card: Card, code: str):
        index = 0
        for i, codes in enumerate(card.get_lists()[0]):
            if codes == code:
                index = i
                break

        for field in card.get_lists():
            field.pop(index)
        card.ids.panel_layout.children[0].close_panel(card.ids.panel_layout.children[0], True)
        card.ids.panel_layout.children[0].remove_widget(card.content)
        self._update_fields(card)


class CustomerView(TableView):
    def __init__(self, **kwargs):
        self.database_view = MDApp.get_running_app().customer_view
        self.record_card_type = CustomerCard
        self.record_type = Customer
        super().__init__(**kwargs)


class WorkerView(TableView):
    def __init__(self, **kwargs):
        self.database_view = MDApp.get_running_app().worker_view
        self.record_card_type = WorkerCard
        self.record_type = Worker
        super().__init__(**kwargs)


class WorkView(TableView):
    def __init__(self, **kwargs):
        self.database_view = MDApp.get_running_app().work_view
        self.record_card_type = WorkCard
        self.record_type = Work
        super().__init__(**kwargs)


class SPTView(TableView):
    def __init__(self, **kwargs):
        self.database_view = MDApp.get_running_app().spt_view
        self.record_card_type = SPTCard
        self.record_type = SPT
        super().__init__(**kwargs)


class SpecificationView(OperationsTableView):
    def __init__(self, **kwargs):
        self.database_view = MDApp.get_running_app().specification_view
        self.record_card_type = SpecificationCard
        self.record_type = Specification
        self.inside_list_cols = 1
        super().__init__(**kwargs)


class TaskView(OperationsTableView):
    def __init__(self, **kwargs):
        self.database_view = MDApp.get_running_app().task_view
        self.record_card_type = TaskCard
        self.record_type = Task
        self.inside_list_cols = 2
        super().__init__(**kwargs)


class KursApp(MDApp):
    kv_directory = './kv'

    def __init__(self, debug=False, backup=True, **kwargs) -> None:
        super().__init__(**kwargs)

        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.accent_palette = 'Red'
        self.theme_cls.accent_hue = '900'
        self.error_color = "#FF0000"
        self.save_color = '#00FF00'

        self.debug = debug
        self.backup = backup

        self.customer_view = CustomerList(debug)
        self.worker_view = Workers(debug)
        self.work_view = WorksCatalog(debug)
        self.spt_view = SPTList(debug)

        self.specification_view = SpecificationList(debug)
        self.task_view = TaskList(debug)

    def auth(self, login: str, password: str) -> None:
        m = hashlib.sha256()
        m.update(password.encode())
        if login == 'admin' and m.hexdigest() == '0ffe1abd1a08215353c233d6e009613e95eec4253832a761af28ff37ac5a150c':
            self.root.current = 'main'

        if not self.backup:
            return

        current_datetime = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        if not os.path.exists(rf'backup/{current_datetime}.db'):
            DataBase(self.debug).backup(rf'backup/{current_datetime}.db')

    def add(self, table_view: BaseDataBaseView, record: BaseRecord):
        table_view.add(record)

    def delete_customer(self, card: Card):
        self.customer_view.delete(card.id)
        self.root.ids.customer_list.records_list.remove_widget(card)

    def update_customer(self, card: CustomerCard):
        fields = [widget for widget in card.children[0].children[0].children if isinstance(widget, MDTextField)][::-1]
        self.customer_view.update(card.id, Customer(*[field.text for field in fields]))
        card.id = fields[0].text

    def delete_worker(self, card: Card):
        self.worker_view.delete(card.id)
        self.root.ids.worker_list.records_list.remove_widget(card)

    def update_worker(self, card: WorkerCard):
        fields = [widget for widget in card.children[0].children[0].children if isinstance(widget, MDTextField)][::-1]
        self.worker_view.update(card.id, Worker(*[field.text for field in fields]))
        card.id = fields[0].text

    def delete_work(self, card: Card):
        self.work_view.delete(card.id)
        self.root.ids.work_list.records_list.remove_widget(card)

    def update_work(self, card: WorkerCard):
        fields = [widget for widget in card.children[0].children[0].children if isinstance(widget, MDTextField)][::-1]
        self.work_view.update(card.id, Work(*[field.text for field in fields]))
        card.id = fields[0].text

    def delete_spt(self, card: Card):
        self.spt_view.delete(card.id)
        self.root.ids.spt_list.records_list.remove_widget(card)

    def update_spt(self, card: WorkerCard):
        fields = [widget for widget in card.children[0].children[0].children if isinstance(widget, MDTextField)][::-1]
        self.spt_view.update(card.id, SPT(*[field.text for field in fields]))
        card.id = fields[0].text

    def add_specification(self):
        self.specification_view.add(Specification('', '', '', '', [''], 0))

    def delete_specification(self, card: Card):
        self.specification_view.delete(card.id)
        self.root.ids.specification_list.records_list.remove_widget(card)

    def update_specification(self, card: SpecificationCard):
        fields = [widget.text for widget in card.children[0].children[0].children if isinstance(widget, MDTextField)][::-1]
        work_codes = [widget.text for widget in card.content.children if isinstance(widget, MDTextField)][::-1]
        self.specification_view.update(card.id, Specification(*fields[:4], work_codes, *fields[4:]))
        card.id = fields[0]
        card.workCode = work_codes

    def add_task(self):
        self.task_view.add(Task('', '', '', [''], [''], 0))

    def delete_task(self, card: Card):
        self.task_view.delete(card.id)
        self.root.ids.task_list.records_list.remove_widget(card)

    def update_task(self, card: TaskCard):
        fields = [widget.text for widget in card.children[0].children[0].children if isinstance(widget, MDTextField)][::-1]
        work_codes = [widget.text for widget in card.content.children if isinstance(widget, MDTextField)][::-1]
        self.task_view.update(card.id, Task(*fields[:3], work_codes[::2], work_codes[1::2], *fields[3:]))
        card.id = fields[0]
        card.workCode = work_codes[::2]
        card.workerCode = work_codes[1::2]


# for tests
if __name__ == '__main__':
    application = KursApp(True, False)
    application.run()
