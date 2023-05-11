from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screen import MDScreen
from kivymd.uix.filemanager import MDFileManager
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivymd.toast import toast

import hashlib
import datetime
import os
import pathlib
from dataclasses import astuple
from time import sleep

from views import ListTableView, CustomerView, WorkerView, WorkView, SPTView, SpecificationView, TaskView
from cards import Card
from database_view import CustomerList, Workers, WorksCatalog, SPTList,\
    SpecificationList, TaskList, BaseDataBaseView, BaseRecord, CustomerReport, WorkerReport
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

        self.database = DataBase(self.debug)

        self.customer_view = CustomerList(debug)
        self.worker_view = Workers(debug)
        self.work_view = WorksCatalog(debug)
        self.spt_view = SPTList(debug)

        self.specification_view = SpecificationList(debug)
        self.task_view = TaskList(debug)

        self.customer_report_view = CustomerReport(self.task_view, self.specification_view, debug)
        self.worker_report_view = WorkerReport(self.worker_view, self.task_view, self.work_view, debug)

        self.is_manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
        self.loading_screen = None
        self.current_datetime = None

    def auth(self, login: str, password: str) -> None:
        m = hashlib.sha256()
        m.update(password.encode())
        if login == 'admin' and m.hexdigest() == '0ffe1abd1a08215353c233d6e009613e95eec4253832a761af28ff37ac5a150c':
            self.root.current = 'main'

            if not self.backup:
                return

            self.current_datetime = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            if not os.path.exists(rf'backup/{self.current_datetime}.db'):
                self.show_loading('Создание точки восстановления')
                Clock.schedule_once(self.database_backup, )
        else:
            toast('Неверные данные для входа')

    def database_backup(self, dt) -> None:
        self.database.backup(rf'backup/{self.current_datetime}.db')
        sleep(5)
        self.hide_loading()

    def show_loading(self, text: str) -> None:
        self.loading_screen = Popup(
            title='',
            auto_dismiss=False,
            title_color=self.theme_cls.text_color,
            separator_color=(0, 0, 0, 0),
            background='',
            background_color=(0, 0, 0, 0.5),
            content=MDFloatLayout(
                MDFloatLayout(
                    MDLabel(
                        text=text,
                        size_hint_x=0.85,
                        pos_hint={"center_x": 0.5, "center_y": 0.9},
                    ),
                    MDBoxLayout(
                        padding=20,
                        size_hint=(0.9, None),
                        height=3,
                        pos_hint={"center_x": 0.5, "center_y": 0.8},
                        md_bg_color=self.theme_cls.primary_color,
                    ),
                    MDLabel(
                        text='Выполнение операции...',
                        size_hint_x=0.85,
                        pos_hint={"center_x": 0.5, "center_y": 0.4},
                    ),
                    size_hint=(0.5, 0.3),
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    md_bg_color=self.theme_cls.bg_normal,
                    padding=20,
                )
            ),
        )
        self.loading_screen.open()

    def hide_loading(self) -> None:
        self.loading_screen.dismiss()
        self.loading_screen = None

    def file_manager_open(self):
        self.file_manager.show(str(pathlib.Path(os.getcwd() + '/backup/')))
        self.is_manager_open = True

    def select_path(self, path):
        toast(path)
        DataBase(self.debug).restore(path)
        self.exit_manager()

    def exit_manager(self, *args):
        self.is_manager_open = False
        self.file_manager.close()

    def exit(self) -> None:
        self.stop()

    def add(self, table_view: BaseDataBaseView, record: BaseRecord):
        table_view.add(record)

    def delete(self, records_list, card: Card):
        self.task_view.delete(card.id)
        records_list.remove_widget(card)

    def update(self, record_view: ListTableView, card: Card):
        fields = [widget.text for widget in card.children[0].children if isinstance(widget, MDTextField)][::-1]
        work_codes = []
        if card.get_lists():
            list_fields = [widget.text for widget in card.content.children if isinstance(widget, MDTextField)][::-1]
            for i in range(len(card.get_lists())):
                work_codes.append(list_fields[i::len(card.get_lists())])
        try:
            limiter_pos = astuple(record_view.record_type()).index([])
        except ValueError:
            limiter_pos = 0
        record_view.database_view.update(card.id, record_view.record_type(*fields[:limiter_pos], *work_codes, *fields[limiter_pos:]))
        card.id = fields[0]
        for i, field in enumerate(card.get_lists()):
            field.clear()
            field.extend(work_codes[i])


# for tests
if __name__ == '__main__':
    application = KursApp(True, False)
    application.run()
