from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

import hashlib
import datetime
import os

from views import CustomerView, WorkerView, WorkView, SPTView, SpecificationView, TaskView
from cards import Card, CustomerCard, WorkerCard, WorkCard, SpecificationCard, TaskCard
from database_view import CustomerList, Customer, Workers, Worker, WorksCatalog, Work, SPTList, SPT,\
    SpecificationList, Specification, TaskList, Task, BaseDataBaseView, BaseRecord
from database import DataBase


class Menu(MDNavigationDrawer):
    pass


class Navigation(MDTopAppBar):
    pass


class MainScreen(MDScreen):
    pass


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
