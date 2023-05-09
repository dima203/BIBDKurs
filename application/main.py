from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.expansionpanel import MDExpansionPanelOneLine, MDExpansionPanel
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivy.properties import StringProperty, NumericProperty, ListProperty, ObjectProperty
from kivy.animation import Animation

import hashlib

from database_view import CustomerList, Customer, Workers, Worker, WorksCatalog, Work, SPTList, SPT,\
    SpecificationList, Specification, TaskList, Task


class Menu(MDNavigationDrawer):
    pass


class Navigation(MDTopAppBar):
    pass


class Card(MDCard):
    id = StringProperty()


class CustomerCard(Card):
    customerCode = StringProperty()
    customerName = StringProperty()
    customerLocation = StringProperty()
    customerPhone = StringProperty()


class WorkerCard(Card):
    workerCode = StringProperty()
    workerFIO = StringProperty()
    professionCode = StringProperty()
    hireDate = StringProperty()
    workerLocation = StringProperty()
    workerPhone = StringProperty()


class WorkCard(Card):
    workCode = StringProperty()
    workPrice = NumericProperty()
    workTime = NumericProperty()


class SPTCard(Card):
    sptCode = StringProperty()
    sptName = StringProperty()
    sptIzm = StringProperty()
    sptPrice = NumericProperty()


class SpecificationCard(Card):
    specificationCode = StringProperty()
    contractCode = StringProperty()
    customerCode = StringProperty()
    sptCode = StringProperty()
    workCode = ListProperty()
    content = ObjectProperty()
    cost = NumericProperty()


class TaskCard(Card):
    taskCode = StringProperty()
    contractCode = StringProperty()
    taskDate = StringProperty()
    workCode = ListProperty()
    workerCode = ListProperty()
    content = ObjectProperty()
    taskCost = NumericProperty()


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


class CustomerView(MDScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.customers: list = MDApp.get_running_app().customer_view.get_table()
        self.customer_list = MDGridLayout(cols=1, spacing=10, size_hint_y=None, padding=20)
        self.customer_list.bind(minimum_height=self.customer_list.setter('height'))
        self.add_button = AddButton(self.add, text='Добавить')

        for customer in self.customers:
            card = CustomerCard(
                id=f'{customer.customerCode}',
                customerCode=customer.customerCode,
                customerName=customer.customerName,
                customerLocation=customer.customerLocation,
                customerPhone=customer.customerPhone,
                size_hint_y=None,
                height=100
            )
            self.customer_list.add_widget(card)
        self.customer_list.add_widget(self.add_button)

        self.add_widget(self.customer_list)

    def add(self) -> None:
        MDApp.get_running_app().add_customer()
        self.customer_list.remove_widget(self.add_button)
        card = CustomerCard(
            id=f'',
            customerCode='',
            customerName='',
            customerLocation='',
            customerPhone='',
            size_hint_y=None,
            height=100
        )
        self.customer_list.add_widget(card)
        self.customer_list.add_widget(self.add_button)


class WorkerView(MDScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.workers: list = MDApp.get_running_app().worker_view.get_table()
        self.worker_list = MDGridLayout(cols=1, spacing=10, size_hint_y=None, padding=20)
        self.worker_list.bind(minimum_height=self.worker_list.setter('height'))
        self.add_button = AddButton(self.add, text='Добавить')

        for worker in self.workers:
            card = WorkerCard(
                id=f'{worker.workerCode}',
                workerCode=worker.workerCode,
                workerFIO=worker.workerFIO,
                professionCode=worker.professionCode,
                hireDate=worker.hireDate,
                workerLocation=worker.workerLocation,
                workerPhone=worker.workerPhone,
                size_hint_y=None,
                height=100
            )
            self.worker_list.add_widget(card)
        self.worker_list.add_widget(self.add_button)

        self.add_widget(self.worker_list)

    def add(self) -> None:
        MDApp.get_running_app().add_worker()
        self.worker_list.remove_widget(self.add_button)
        card = WorkerCard(
            id=f'',
            workerCode='',
            workerFIO='',
            professionCode='',
            hireDate='',
            workerLocation='',
            workerPhone='',
            size_hint_y=None,
            height=100
        )
        self.worker_list.add_widget(card)
        self.worker_list.add_widget(self.add_button)


class WorkView(MDScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.works: list = MDApp.get_running_app().work_view.get_table()
        self.work_list = MDGridLayout(cols=1, spacing=10, size_hint_y=None, padding=20)
        self.work_list.bind(minimum_height=self.work_list.setter('height'))
        self.add_button = AddButton(self.add, text='Добавить')

        for work in self.works:
            card = WorkCard(
                id=f'{work.workCode}',
                workCode=work.workCode,
                workPrice=work.workPrice,
                workTime=work.workTime,
                size_hint_y=None,
                height=100
            )
            self.work_list.add_widget(card)
        self.work_list.add_widget(self.add_button)

        self.add_widget(self.work_list)

    def add(self) -> None:
        MDApp.get_running_app().add_work()
        self.work_list.remove_widget(self.add_button)
        card = WorkCard(
            id=f'',
            workCode='',
            workPrice='0',
            workTime='0',
            size_hint_y=None,
            height=100
        )
        self.work_list.add_widget(card)
        self.work_list.add_widget(self.add_button)


class SPTView(MDScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.spts: list = MDApp.get_running_app().spt_view.get_table()
        self.spt_list = MDGridLayout(cols=1, spacing=10, size_hint_y=None, padding=20)
        self.spt_list.bind(minimum_height=self.spt_list.setter('height'))
        self.add_button = AddButton(self.add, text='Добавить')

        for spt in self.spts:
            card = SPTCard(
                id=f'{spt.sptCode}',
                sptCode=spt.sptCode,
                sptName=spt.sptName,
                sptIzm=spt.sptIzm,
                sptPrice=spt.sptPrice,
                size_hint_y=None,
                height=100
            )
            self.spt_list.add_widget(card)
        self.spt_list.add_widget(self.add_button)

        self.add_widget(self.spt_list)

    def add(self) -> None:
        MDApp.get_running_app().add_spt()
        self.spt_list.remove_widget(self.add_button)
        card = SPTCard(
            id=f'',
            sptCode='',
            sptName='',
            sptIzm='',
            sptPrice='0',
            size_hint_y=None,
            height=100
        )
        self.spt_list.add_widget(card)
        self.spt_list.add_widget(self.add_button)


class SpecificationView(MDScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.specifications: list = MDApp.get_running_app().specification_view.get_table()
        self.specification_list = MDGridLayout(cols=1, spacing=10, size_hint_y=None, padding=20)
        self.specification_list.bind(minimum_height=self.specification_list.setter('height'))
        self.add_button = AddButton(self.add, text='Добавить')

        for specification in self.specifications:
            card = SpecificationCard(
                id=f'{specification.specificationCode}',
                specificationCode=specification.specificationCode,
                contractCode=specification.contractCode,
                customerCode=specification.customerCode,
                sptCode=specification.sptCode,
                workCode=specification.workCode,
                content=MDGridLayout(
                    size_hint_y=None,
                    adaptive_height=True,
                    cols=2,
                ),
                cost=specification.cost,
                size_hint_y=None,
            )

            card.ids.panel_layout.add_widget(MDExpansionPanel(
                icon="plus",
                content=card.content,
                panel_cls=MDExpansionPanelOneLine(
                    text="Список работ",
                    on_release=(lambda _: self.update_specification_fields(card))
                )
            ))
            self.update_specification_fields(card)
            self.specification_list.add_widget(card)
        self.specification_list.add_widget(self.add_button)

        self.add_widget(self.specification_list)

    def update_specification_fields(self, card: SpecificationCard):
        card.content.clear_widgets()

        for workCode in card.workCode:
            card.content.add_widget(MDTextField(text=workCode))
            card.content.add_widget(DeleteWorkCodeButton(self.delete_work_code, card, workCode))
        card.content.add_widget(ListAddButton(self.add_work_code, card, text='Добавить'))
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

    def add_work_code(self, card: SpecificationCard):
        card.workCode.append('')
        card.ids.panel_layout.children[0].close_panel(card.ids.panel_layout.children[0], True)
        card.ids.panel_layout.children[0].remove_widget(card.content)
        self.update_specification_fields(card)

    def delete_work_code(self, card: SpecificationCard, work_code: str):
        card.workCode.remove(work_code)
        card.ids.panel_layout.children[0].close_panel(card.ids.panel_layout.children[0], True)
        card.ids.panel_layout.children[0].remove_widget(card.content)
        self.update_specification_fields(card)

    def add(self) -> None:
        MDApp.get_running_app().add_specification()
        self.specification_list.remove_widget(self.add_button)
        card = SpecificationCard(
            id=f'',
            specificationCode='',
            contractCode='',
            customerCode='',
            sptCode='',
            workCode=[],
            content=MDGridLayout(
                size_hint_y=None,
                adaptive_height=True,
                cols=2,
            ),
            cost=0,
            size_hint_y=None,
        )

        card.ids.panel_layout.add_widget(MDExpansionPanel(
            icon="plus",
            content=card.content,
            panel_cls=MDExpansionPanelOneLine(
                text="Список работ",
                on_release=(lambda _: self.update_specification_fields(card))
            )
        ))

        self.update_specification_fields(card)
        self.specification_list.add_widget(card)
        self.specification_list.add_widget(self.add_button)


class TaskView(MDScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.tasks: list = MDApp.get_running_app().task_view.get_table()
        self.task_list = MDGridLayout(cols=1, spacing=10, size_hint_y=None, padding=20)
        self.task_list.bind(minimum_height=self.task_list.setter('height'))
        self.add_button = AddButton(self.add, text='Добавить')

        for task in self.tasks:
            card = TaskCard(
                id=f'{task.taskCode}',
                taskCode=task.taskCode,
                contractCode=task.contractCode,
                taskDate=task.taskDate,
                workCode=task.workCode,
                workerCode=task.workerCode,
                content=MDGridLayout(
                    spacing=10,
                    size_hint_y=None,
                    adaptive_height=True,
                    cols=3
                ),
                taskCost=task.taskCost,
                size_hint_y=None,
            )

            card.ids.panel_layout.add_widget(MDExpansionPanel(
                icon="plus",
                content=card.content,
                panel_cls=MDExpansionPanelOneLine(
                    text="Список работ",
                    on_release=(lambda _: self.update_task_fields(card))
                )
            ))
            self.update_task_fields(card)
            self.task_list.add_widget(card)
        self.task_list.add_widget(self.add_button)

        self.add_widget(self.task_list)

    def update_task_fields(self, card: TaskCard):
        card.content.clear_widgets()

        for i in range(len(card.workCode)):
            card.content.add_widget(MDTextField(text=card.workCode[i]))
            card.content.add_widget(MDTextField(text=card.workerCode[i]))
            card.content.add_widget(DeleteWorkCodeButton(self.delete_work_code, card, card.workCode[i]))
        card.content.add_widget(ListAddButton(self.add_work_worker_code, card, text='Добавить'))
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

    def add_work_worker_code(self, card: TaskCard):
        card.workCode.append('')
        card.workerCode.append('')
        card.ids.panel_layout.children[0].close_panel(card.ids.panel_layout.children[0], True)
        card.ids.panel_layout.children[0].remove_widget(card.content)
        self.update_task_fields(card)
        card.ids.panel_layout.children[0].open_panel()

    def delete_work_code(self, card: TaskCard, work_code: str):
        index = card.workCode.index(work_code)
        card.workCode.pop(index)
        card.workerCode.pop(index)
        card.ids.panel_layout.children[0].close_panel(card.ids.panel_layout.children[0], True)
        card.ids.panel_layout.children[0].remove_widget(card.content)
        self.update_task_fields(card)
        card.ids.panel_layout.children[0].open_panel()

    def add(self) -> None:
        MDApp.get_running_app().add_task()
        self.task_list.remove_widget(self.add_button)
        card = TaskCard(
            id=f'',
            taskCode='',
            contractCode='',
            taskDate='',
            workCode=[],
            workerCode=[],
            content=MDGridLayout(
                spacing=10,
                size_hint_y=None,
                adaptive_height=True,
                cols=3
            ),
            taskCost=0,
            size_hint_y=None,
        )
        card.ids.panel_layout.add_widget(MDExpansionPanel(
            icon="plus",
            content=card.content,
            panel_cls=MDExpansionPanelOneLine(
                text="Список работ",
                on_release=(lambda _: self.update_task_fields(card))
            )
        ))
        self.update_task_fields(card)
        self.task_list.add_widget(card)
        self.task_list.add_widget(self.add_button)


class KursApp(MDApp):
    kv_directory = './kv'

    def __init__(self, debug=False, **kwargs) -> None:
        super().__init__(**kwargs)

        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.accent_palette = 'Red'
        self.theme_cls.accent_hue = '900'
        self.error_color = "#FF0000"
        self.save_color = '#00FF00'

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

    def add_customer(self):
        self.customer_view.add(Customer('', '', '', ''))

    def delete_customer(self, card: Card):
        self.customer_view.delete(card.id)
        self.root.ids.customer_list.customer_list.remove_widget(card)

    def update_customer(self, card: CustomerCard):
        fields = [widget for widget in card.children[0].children[0].children if isinstance(widget, MDTextField)][::-1]
        self.customer_view.update(card.id, Customer(*[field.text for field in fields]))
        card.id = fields[0].text

    def add_worker(self):
        self.worker_view.add(Worker('', '', '', '', '', ''))

    def delete_worker(self, card: Card):
        self.worker_view.delete(card.id)
        self.root.ids.worker_list.worker_list.remove_widget(card)

    def update_worker(self, card: WorkerCard):
        fields = [widget for widget in card.children[0].children[0].children if isinstance(widget, MDTextField)][::-1]
        self.worker_view.update(card.id, Worker(*[field.text for field in fields]))
        card.id = fields[0].text

    def add_work(self):
        self.work_view.add(Work('', 0, 0))

    def delete_work(self, card: Card):
        self.work_view.delete(card.id)
        self.root.ids.work_list.work_list.remove_widget(card)

    def update_work(self, card: WorkerCard):
        fields = [widget for widget in card.children[0].children[0].children if isinstance(widget, MDTextField)][::-1]
        self.work_view.update(card.id, Work(*[field.text for field in fields]))
        card.id = fields[0].text

    def add_spt(self):
        self.spt_view.add(SPT('', '', '', 0))

    def delete_spt(self, card: Card):
        self.spt_view.delete(card.id)
        self.root.ids.spt_list.spt_list.remove_widget(card)

    def update_spt(self, card: WorkerCard):
        fields = [widget for widget in card.children[0].children[0].children if isinstance(widget, MDTextField)][::-1]
        self.spt_view.update(card.id, SPT(*[field.text for field in fields]))
        card.id = fields[0].text

    def add_specification(self):
        self.specification_view.add(Specification('', '', '', '', [''], 0))

    def delete_specification(self, card: Card):
        self.specification_view.delete(card.id)
        self.root.ids.specification_list.specification_list.remove_widget(card)

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
        self.root.ids.task_list.task_list.remove_widget(card)

    def update_task(self, card: TaskCard):
        fields = [widget.text for widget in card.children[0].children[0].children if isinstance(widget, MDTextField)][::-1]
        work_codes = [widget.text for widget in card.content.children if isinstance(widget, MDTextField)][::-1]
        self.task_view.update(card.id, Task(*fields[:3], work_codes[::2], work_codes[1::2], *fields[3:]))
        card.id = fields[0]
        card.workCode = work_codes[::2]
        card.workerCode = work_codes[1::2]


# for tests
if __name__ == '__main__':
    application = KursApp(True)
    application.run()
