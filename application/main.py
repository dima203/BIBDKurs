from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.filemanager import MDFileManager
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivymd.toast import toast
from kivy.lang import Builder

import hashlib
import datetime
import os
from dataclasses import astuple
from time import sleep
import asyncio

from .views import ListTableView
from .cards import Card
from database_view import CustomerList, Workers, WorksCatalog, SPTList,\
    SpecificationList, TaskList, BaseDataBaseView, BaseRecord, CustomerReport, WorkerReport, AllReport, ContractReport
from database import DataBase


class Menu(MDNavigationDrawer):
    pass


class Navigation(MDTopAppBar):
    pass


class LoadingScreen(MDScreen):
    pass


class AuthScreen(MDScreen):
    pass


class MainScreen(MDScreen):
    pass


class TablesScreen(MDScreen):
    pass


class OperationTablesScreen(MDScreen):
    pass


class ReportScreen(MDScreen):
    pass


class RestoreScreen(MDScreen):
    pass


class MainScreenManager(MDScreenManager):
    id = 'main_screen_manager'


class KursApp(MDApp):
    kv_directory = './application/kv'

    def __init__(self, debug=False, backup=True, **kwargs):
        super().__init__(**kwargs)

        self.debug = debug
        self.backup = backup

    def build(self, **kwargs):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.accent_palette = 'Red'
        self.theme_cls.accent_hue = '900'
        self.error_color = "#FF0000"
        self.save_color = '#00FF00'

        self.screen_manager = MainScreenManager()
        self.loading()
        return self.screen_manager

    def on_start(self):
        Clock.schedule_once(self.start, 5)

    def loading(self) -> None:
        Builder.load_file(self.kv_directory + '/loader.kv')
        self.screen_manager.add_widget(LoadingScreen())
        self.screen_manager.current = 'loading'

    def start(self, dt):
        self.database = DataBase(self.debug)
        self.root.do_layout()

        self.customer_view = CustomerList(self.debug)
        self.worker_view = Workers(self.debug)
        self.work_view = WorksCatalog(self.debug)
        self.spt_view = SPTList(self.debug)

        self.specification_view = SpecificationList(self.debug)
        self.task_view = TaskList(self.debug)

        self.customer_report_view = CustomerReport(self.task_view, self.specification_view, self.debug)
        self.worker_report_view = WorkerReport(self.worker_view, self.task_view, self.work_view, self.debug)
        self.all_report_view = AllReport(self.task_view, self.specification_view, self.debug)
        self.contract_report_view = ContractReport(self.task_view, self.specification_view,
                                                   self.work_view, self.customer_view, self.debug)

        self.is_manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
        self.loading_screen = None
        self.current_datetime = None

        Builder.load_file(self.kv_directory + '/main.kv')
        self.root.add_widget(AuthScreen())
        self.root.add_widget(MainScreen())
        self.root.add_widget(TablesScreen())
        self.root.add_widget(OperationTablesScreen())
        self.root.add_widget(ReportScreen())
        self.root.add_widget(RestoreScreen())
        self.root.current = 'auth'

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
        self.file_manager.show(str(os.getcwd() + '/backup/'))
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
