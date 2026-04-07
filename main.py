import json, os, base64, threading, time, requests, urllib3
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
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock
from kivy.app import App
from kivy.utils import platform

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- FONT ---
FONT_FILE = "bpg_arial.ttf"
if os.path.exists(FONT_FILE):
    LabelBase.register(name="Roboto", fn_regular=FONT_FILE)
    LabelBase.register(name="GeorgianFont", fn_regular=FONT_FILE)
    USED_FONT = "GeorgianFont"
else:
    USED_FONT = "Roboto"

def get_path(filename):
    try:
        base_path = App.get_running_app().user_data_dir
        if not os.path.exists(base_path): os.makedirs(base_path)
        return os.path.join(base_path, filename)
    except: return filename

API_DATA = {"u": "RSS", "p": "zLdNY8JkBi", "c": "1160", "s": "3167", "h": "FZf3eNx@ZJE", "sd": "RSS-BUS"}
API_BASE_URL = "https://bi.msg.ge/sendsms.php"

KV = f'''
<StopRow>:
    orientation: "horizontal"
    padding: "10dp"
    spacing: "10dp"
    size_hint_y: None
    height: dp(80)
    canvas.before:
        Color:
            rgba: (0.12, 0.12, 0.12, 1) if app.theme_cls.theme_style == "Dark" else (0.95, 0.95, 0.95, 1)
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [15,]
    
    MDIcon:
        icon: "circle"
        theme_text_color: "Custom"
        text_color: root.status_color
        size_hint_x: None
        width: "20dp"
        pos_hint: {{"center_y": .5}}

    MDBoxLayout:
        orientation: "vertical"
        adaptive_height: True
        pos_hint: {{"center_y": .5}}
        MDLabel:
            text: root.name
            bold: True
            font_style: "Subtitle1"
            shorten: True
        MDLabel:
            text: root.phone
            theme_text_color: "Hint"
            font_style: "Caption"
    
    MDBoxLayout:
        adaptive_width: True
        spacing: "2dp"
        MDIconButton:
            icon: "pencil-outline"
            icon_size: "20sp"
            on_release: app.show_edit_dialog(root.phone, root.name)
        MDIconButton:
            icon: "play-outline"
            icon_size: "24sp"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
            on_release: app.fire_single(root.phone, root.name, "ON")
        MDIconButton:
            icon: "stop-outline"
            icon_size: "24sp"
            theme_text_color: "Custom"
            text_color: 1, 0.3, 0.3, 1
            on_release: app.fire_single(root.phone, root.name, "OFF")
        MDIconButton:
            icon: "trash-can-outline"
            icon_size: "20sp"
            on_release: app.remove_unit(root.phone)

ScreenManager:
    LoginScreen:
    MainScreen:
    SettingsScreen:
    DatabaseScreen:
    HistoryScreen:

<LoginScreen>:
    name: "login"
    MDBoxLayout:
        orientation: "vertical"
        padding: "40dp"
        md_bg_color: self.theme_cls.bg_normal
        Widget:
        MDIcon:
            icon: "bus-clock"
            pos_hint: {{"center_x": .5}}
            font_size: "100sp"
            theme_text_color: "Primary"
        MDLabel:
            text: "RSS BUS CONTROL"
            halign: "center"
            font_style: "H5"
            bold: True
        Widget:
            size_hint_y: None
            height: "30dp"
        MDTextField:
            id: pin_input
            hint_text: "PIN CODE"
            password: True
            mode: "rectangle"
            on_text_validate: app.check_login(self.text)
        MDFillRoundFlatIconButton:
            text: "LOG IN"
            icon: "login"
            size_hint_x: 1
            on_release: app.check_login(pin_input.text)
        Widget:

<DatabaseScreen>:
    name: "database"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "ნომრების ბაზა"
            left_action_items: [["arrow-left", lambda x: app.change_screen("settings")]]
            right_action_items: [["plus", lambda x: app.show_add_dialog()]]
        
        MDBoxLayout:
            size_hint_y: None
            height: "60dp"
            padding: "10dp"
            MDTextField:
                id: search_field
                hint_text: "ძებნა..."
                mode: "line"
                on_text: app.refresh_ui(self.text)
                icon_left: "magnify"
        
        RecycleView:
            id: rv
            viewclass: 'StopRow'
            RecycleBoxLayout:
                default_size: None, dp(80)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
                spacing: dp(10)
                padding: dp(10)

<MainScreen>:
    name: "main"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "RSS COMMANDER"
            right_action_items: [["history", lambda x: app.change_screen("history")], ["cog", lambda x: app.change_screen("settings")]]
        MDBoxLayout:
            orientation: "vertical"
            padding: "25dp"
            spacing: "20dp"
            MDCard:
                id: status_card
                size_hint_y: None
                height: "140dp"
                radius: 20
                md_bg_color: app.theme_cls.primary_dark
                MDBoxLayout:
                    orientation: "vertical"
                    padding: "15dp"
                    MDIcon:
                        id: status_icon
                        icon: "shield-check"
                        halign: "center"
                        font_size: "40sp"
                    MDLabel:
                        id: live_node_name
                        text: "სისტემა მზად არის"
                        halign: "center"
                        bold: True
                    MDLabel:
                        id: live_status_text
                        text: "მოთხოვნის მოლოდინში"
                        halign: "center"
                        theme_text_color: "Hint"
            MDFillRoundFlatIconButton:
                text: "ყველას ჩართვა (ON)"
                icon: "power"
                size_hint_x: 1
                height: "55dp"
                on_release: app.confirm_action("ON")
            MDFillRoundFlatIconButton:
                text: "ყველას გათიშვა (OFF)"
                icon: "power-off"
                size_hint_x: 1
                height: "55dp"
                md_bg_color: 0.8, 0.2, 0.2, 1
                on_release: app.confirm_action("OFF")
            Widget:

<HistoryScreen>:
    name: "history"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "ისტორია"
            left_action_items: [["arrow-left", lambda x: app.change_screen("main")]]
            right_action_items: [["delete-sweep", lambda x: app.clear_history()]]
        ScrollView:
            MDList:
                id: history_list

<SettingsScreen>:
    name: "settings"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "პარამეტრები"
            left_action_items: [["arrow-left", lambda x: app.change_screen("main")]]
        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: "20dp"
                spacing: "15dp"
                size_hint_y: None
                height: self.minimum_height
                MDFillRoundFlatIconButton:
                    text: "ბაზის მართვა"
                    icon: "database"
                    size_hint_x: 1
                    on_release: app.change_screen("database")
                MDSeparator:
                MDTextField:
                    id: new_pin
                    hint_text: "ახალი PIN კოდი"
                    password: True
                MDFillRoundFlatIconButton:
                    text: "შენახვა"
                    icon: "check"
                    size_hint_x: 1
                    on_release: app.save_settings()
                MDFillRoundFlatIconButton:
                    text: "თემის შეცვლა"
                    icon: "palette"
                    size_hint_x: 1
                    on_release: app.toggle_theme()

'''

class StopRow(BoxLayout):
    name = StringProperty()
    phone = StringProperty()
    status_color = ColorProperty([0.5, 0.5, 0.5, 1])

class LoginScreen(Screen): pass
class MainScreen(Screen): pass
class SettingsScreen(Screen): pass
class DatabaseScreen(Screen): pass
class HistoryScreen(Screen): pass

class RSSApp(MDApp):
    def build(self):
        self.db = self.load_db()
        self.history = self.load_history()
        self.theme_cls.theme_style = self.db.get("theme", "Dark")
        self.theme_cls.primary_palette = "Cyan"
        self.dia = None
        return Builder.load_string(KV)

    def load_db(self):
        path = get_path("config.dat")
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    return json.loads(base64.b64decode(f.read()).decode())
            except: pass
        return {"nums": {}, "pin": "1234", "theme": "Dark"}

    def save_db(self):
        def _save():
            path = get_path("config.dat")
            data = base64.b64encode(json.dumps(self.db).encode())
            with open(path, "wb") as f: f.write(data)
        threading.Thread(target=_save, daemon=True).start()

    def check_login(self, pin):
        if pin == self.db.get("pin"): self.root.current = "main"
        else: self.root.get_screen("login").ids.pin_input.error = True

    def refresh_ui(self, query=""):
        rv = self.root.get_screen("database").ids.rv
        q = query.lower()
        rv.data = [
            {'name': n, 'phone': p, 'status_color': [0.5, 0.5, 0.5, 1]} 
            for p, n in self.db["nums"].items() 
            if q in n.lower() or q in p
        ]

    def change_screen(self, name):
        self.root.current = name
        if name == "database": self.refresh_ui()

    def show_add_dialog(self):
        self.close_dia()
        content = BoxLayout(orientation='vertical', spacing="10dp", size_hint_y=None, height="120dp")
        self.ni = MDTextField(hint_text="სახელი")
        self.pi = MDTextField(hint_text="ტელეფონი", input_filter="int")
        content.add_widget(self.ni); content.add_widget(self.pi)
        self.dia = MDDialog(title="დამატება", type="custom", content_cls=content,
                            buttons=[MDFlatButton(text="გაუქმება", on_release=self.close_dia),
                                     MDRaisedButton(text="შენახვა", on_release=lambda x: self.add_unit())])
        self.dia.open()

    def add_unit(self):
        if self.ni.text and self.pi.text:
            self.db["nums"][self.pi.text] = self.ni.text
            self.save_db()
            self.refresh_ui()
        self.close_dia()

    def remove_unit(self, phone):
        if phone in self.db["nums"]:
            del self.db["nums"][phone]
            self.save_db()
            self.refresh_ui()

    def close_dia(self, *args):
        if self.dia: self.dia.dismiss()

    def toggle_theme(self):
        self.theme_cls.theme_style = "Light" if self.theme_cls.theme_style == "Dark" else "Dark"
        self.db["theme"] = self.theme_cls.theme_style
        self.save_db()

    def save_settings(self):
        s = self.root.get_screen("settings").ids
        if s.new_pin.text: self.db["pin"] = s.new_pin.text
        self.save_db()
        self.root.current = "main"

    # --- API LOGIC (Simplified for speed) ---
    def fire_single(self, phone, name, cmd):
        self.root.current = "main"
        threading.Thread(target=self._api_call, args=(phone, name, cmd), daemon=True).start()

    def _api_call(self, phone, name, cmd):
        Clock.schedule_once(lambda dt: self.update_status(name, "გაგზავნა...", [0.8, 0.5, 0, 1], "transmit"))
        params = {"username": API_DATA['u'], "password": API_DATA['p'], "to": phone, "text": f"1234#{cmd}#"}
        try:
            r = requests.get(API_BASE_URL, params=params, timeout=5, verify=False)
            status = "წარმატებით ✅" if "0000" in r.text else "შეცდომა ❌"
            color = [0, 0.6, 0.3, 1] if "0000" in r.text else [0.8, 0.2, 0.2, 1]
            icon = "check-circle" if "0000" in r.text else "alert-circle"
        except:
            status, color, icon = "კავშირის შეცდომა", [0.8, 0.2, 0.2, 1], "wifi-off"
        
        Clock.schedule_once(lambda dt: self.update_status(name, status, color, icon))

    def update_status(self, name, text, color, icon):
        ui = self.root.get_screen("main").ids
        ui.live_node_name.text = name
        ui.live_status_text.text = text
        ui.status_card.md_bg_color = color
        ui.status_icon.icon = icon

    def load_history(self): return [] # Placeholder
    def clear_history(self): pass
    def confirm_action(self, cmd): pass # Batch logic here

if __name__ == "__main__":
    RSSApp().run()
