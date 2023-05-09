from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton
from kivy.properties import StringProperty, NumericProperty

from database_view import CustomerList, Customer, Workers, Worker, WorksCatalog, Work, SPTList, SPT


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


class AddButton(MDRectangleFlatButton):
    def __init__(self, callback, **kwargs) -> None:
        super().__init__(**kwargs)
        self.callback = callback

    def on_press(self):
        self.callback()


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


# for tests
if __name__ == '__main__':
    application = KursApp(True)
    application.run()
