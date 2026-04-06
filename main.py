import json, os, base64, threading, time, requests, urllib3, certifi
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton, MDFillRoundFlatIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivymd.uix.progressbar import MDProgressBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty, ColorProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.app import App
from kivy.utils import platform

# SSL და ინტერნეტის ფიქსი
os.environ['SSL_CERT_FILE'] = certifi.where()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# შრიფტის უსაფრთხო ჩატვირთვა
FONT_FILE = "bpg_arial.ttf"
if os.path.exists(FONT_FILE):
    LabelBase.register(name="Roboto", fn_regular=FONT_FILE)
    LabelBase.register(name="GeorgianFont", fn_regular=FONT_FILE)
    USED_FONT = "GeorgianFont"
else:
    USED_FONT = "Roboto"

def get_path(filename):
    if platform == 'android':
        from android.storage import app_storage_path
        base_path = app_storage_path()
    else:
        base_path = "."
    if not os.path.exists(base_path): os.makedirs(base_path, exist_ok=True)
    return os.path.join(base_path, filename)

# API და KV მონაცემები (შენი ორიგინალი ლოგიკა)
API_DATA = {"u": "RSS", "p": "zLdNY8JkBi", "c": "1160", "s": "3167", "h": "FZf3eNx@ZJE", "sd": "RSS-BUS"}
API_BASE_URL = "https://bi.msg.ge/sendsms.php"

KV = '''
ScreenManager:
    LoginScreen:
    MainScreen:
<LoginScreen>:
    name: "login"
    MDBoxLayout:
        orientation: "vertical"
        padding: "40dp"
        spacing: "20dp"
        MDIcon:
            icon: "shield-lock"
            pos_hint: {"center_x": .5}
            font_size: "80sp"
        MDTextField:
            id: pin_input
            hint_text: "PIN"
            password: True
            mode: "rectangle"
        MDFillRoundFlatIconButton:
            text: "LOGIN"
            icon: "login"
            on_release: app.check_login(pin_input.text)
<MainScreen>:
    name: "main"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "RSS COMMANDER"
        MDLabel:
            text: "Welcome to Control Center"
            halign: "center"
'''

class LoginScreen(Screen): pass
class MainScreen(Screen): pass

class RSSMobileApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        return Builder.load_string(KV)

    def check_login(self, pin):
        if pin == "1234": self.root.current = "main"

if __name__ == "__main__":
    RSSMobileApp().run()
