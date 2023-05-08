from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCardSwipe
from kivy.properties import StringProperty

from database_view import CustomerList


class Menu(MDNavigationDrawer):
    pass


class Navigation(MDTopAppBar):
    pass


class CardSwipe(MDCardSwipe):
    id = StringProperty()
    text = StringProperty()


class CustomerView(MDScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.customers: list = MDApp.get_running_app().customer_view.get_table()
        self.customer_list = MDGridLayout(cols=1, spacing=10, size_hint_y=None, padding=20)
        self.customer_list.bind(minimum_height=self.customer_list.setter('height'))

        for customer in self.customers:
            card = CardSwipe(
                id=f'{customer.customerCode}',
                text=f'{customer.customerCode} | {customer.customerName} | {customer.customerLocation} | {customer.customerPhone}',
                size_hint_y=None,
                height=100
            )
            self.customer_list.add_widget(card)

        self.add_widget(self.customer_list)


class KursApp(MDApp):
    kv_directory = './kv'

    def __init__(self, debug=False, **kwargs) -> None:
        super().__init__(**kwargs)

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.accent_hue = '900'
        self.error_text_color = "#FF0000"

        self.customer_view = CustomerList(debug)

    def menu_call(self):
        self.root.ids.nav_drawer.set_state('open')

    def main_button_press(self):
        self.root.ids.nav_drawer.set_state('close')
        self.root.ids.screen_manager.current = 'main'

    def add_account_button_press(self):
        self.root.ids.nav_drawer.set_state('close')
        self.root.ids.screen_manager.current = 'add_account'

    def delete_card(self, card: CardSwipe):
        print(self.customer_view.get(card.id))
        self.customer_view.delete(card.id)
        self.root.ids.customer_list.customer_list.remove_widget(card)


# for tests
if __name__ == '__main__':
    application = KursApp(True)
    application.run()
