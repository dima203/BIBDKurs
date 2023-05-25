import os
import sys


if hasattr(sys, '_MEIPASS'):
    os.environ['KIVY_NO_CONSOLELOG'] = '1'


from application import KursApp


if __name__ == '__main__':
    app = KursApp()
    app.run()
