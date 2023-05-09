from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton
from kivy.properties import StringProperty

from database_view import CustomerList, Customer


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


class CustomerAddButton(MDRectangleFlatButton):
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
        self.add_button = CustomerAddButton(self.add, text='Добавить')

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

    def menu_call(self):
        self.root.ids.nav_drawer.set_state('open')

    def main_button_press(self):
        self.root.ids.nav_drawer.set_state('close')
        self.root.ids.screen_manager.current = 'main'

    def add_customer(self):
        self.customer_view.add(Customer('', '', '', ''))

    def delete_customer(self, card: CustomerCard):
        self.customer_view.delete(card.id)
        self.root.ids.customer_list.customer_list.remove_widget(card)

    def update_customer(self, card: CustomerCard):
        fields = [widget for widget in card.children[0].children[0].children if isinstance(widget, MDTextField)][::-1]
        self.customer_view.update(card.id, Customer(*[field.text for field in fields]))
        card.id = fields[0].text


# for tests
if __name__ == '__main__':
    application = KursApp(True)
    application.run()
