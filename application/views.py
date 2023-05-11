from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivymd.uix.expansionpanel import MDExpansionPanelOneLine, MDExpansionPanel
from kivymd.uix.textfield import MDTextField
from kivy.animation import Animation
from kivymd.toast import toast

from dataclasses import astuple, asdict
from sqlite3 import IntegrityError

from database_view import BaseDataBaseView, BaseRecord, Customer, Worker, Work, SPT, Specification, Task, ReportCustomer
from cards import Card, CustomerCard, WorkerCard, WorkCard, SPTCard, SpecificationCard, TaskCard, CustomerReportCard


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

        for record in self.records:
            self._add_card(record)

        self.add_widget(self.records_list)

    def refresh(self) -> None:
        self.records = self.database_view.get_table()
        self.records_list.clear_widgets()
        for record in self.records:
            self._add_card(record)

    def _add_card(self, record: BaseRecord) -> None:
        card = self.record_card_type(
            id=f'{astuple(record)[0]}',
            **asdict(record),
            size_hint_y=None,
            height=100
        )
        self.records_list.add_widget(card)


class ListTableView(TableView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_button = AddButton(self.add, text='Добавить')
        self.records_list.add_widget(self.add_button)

    def add(self) -> None:
        record = self.record_type()
        try:
            MDApp.get_running_app().add(self.database_view, record)
            self.records_list.remove_widget(self.add_button)
            self._add_card(record)
            self.records_list.add_widget(self.add_button)
        except IntegrityError:
            toast('Сначала сохраните созданную запись')

    def refresh(self) -> None:
        super().refresh()
        self.records_list.add_widget(self.add_button)


class OperationsTableView(ListTableView):
    inside_list_cols: int

    def _add_card(self, record: BaseRecord) -> None:
        card = self.record_card_type(
            id=f'{astuple(record)[0]}',
            **asdict(record),
            content=MDGridLayout(
                size_hint_y=None,
                adaptive_height=True,
                spacing=10,
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
            card.content.add_widget(DeleteWorkCodeButton(
                self._delete_inside_list_record, card, fields[0],
                size_hint_x=None,
                width=50,
            ))

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


class CustomerView(ListTableView):
    def __init__(self, **kwargs):
        self.database_view = MDApp.get_running_app().customer_view
        self.record_card_type = CustomerCard
        self.record_type = Customer
        super().__init__(**kwargs)


class WorkerView(ListTableView):
    def __init__(self, **kwargs):
        self.database_view = MDApp.get_running_app().worker_view
        self.record_card_type = WorkerCard
        self.record_type = Worker
        super().__init__(**kwargs)


class WorkView(ListTableView):
    def __init__(self, **kwargs):
        self.database_view = MDApp.get_running_app().work_view
        self.record_card_type = WorkCard
        self.record_type = Work
        super().__init__(**kwargs)


class SPTView(ListTableView):
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


class CustomerReportView(TableView):
    def __init__(self, **kwargs):
        self.database_view = MDApp.get_running_app().customer_report_view
        self.record_card_type = CustomerReportCard
        self.record_type = ReportCustomer
        super().__init__(**kwargs)
