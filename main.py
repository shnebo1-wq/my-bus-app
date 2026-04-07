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

# --- ANDROID SPECIFIC IMPORTS ---
if platform == 'android':
    from jnius import autoclass
    from android.storage import app_storage_path
    PRIMARY_STORAGE = app_storage_path()
else:
    PRIMARY_STORAGE = "."

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- FONT REGISTRATION ---
FONT_FILE = "bpg_arial.ttf"
if os.path.exists(FONT_FILE):
    LabelBase.register(name="Roboto", fn_regular=FONT_FILE)
    LabelBase.register(name="GeorgianFont", fn_regular=FONT_FILE)
    USED_FONT = "GeorgianFont"
else:
    USED_FONT = "Roboto"

def get_path(filename):
    """ გარანტირებული გზა ფაილების შესანახად Android-ზე """
    try:
        if platform == 'android':
            target_dir = PRIMARY_STORAGE
        else:
            target_dir = App.get_running_app().user_data_dir
            
        if not os.path.exists(target_dir): 
            os.makedirs(target_dir)
        return os.path.join(target_dir, filename)
    except: 
        return filename

# --- API CONFIG ---
API_DATA = {"u": "RSS", "p": "zLdNY8JkBi", "c": "1160", "s": "3167", "h": "FZf3eNx@ZJE", "sd": "RSS-BUS"}
API_BASE_URL = "https://bi.msg.ge/sendsms.php"

# --- KV UI STRING ---
KV = f'''
<StopRow>:
    orientation: "horizontal"
    padding: "12dp"
    spacing: "8dp"
    size_hint_y: None
    height: dp(85)
    canvas.before:
        Color:
            rgba: (0.15, 0.15, 0.15, 1) if app.theme_cls.theme_style == "Dark" else (0.92, 0.92, 0.92, 1)
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [20,]
    
    MDIcon:
        icon: "circle"
        theme_text_color: "Custom"
        text_color: root.status_color
        font_size: "14sp"
        size_hint_x: None
        width: "20dp"
        pos_hint: {{"center_y": .5}}

    MDBoxLayout:
        orientation: "vertical"
        MDLabel:
            text: root.name
            bold: True
            font_style: "Subtitle1"
            shorten: True
        MDLabel:
            text: root.phone
            theme_text_color: "Hint"
            font_style: "Caption"
    
    MDIconButton:
        icon: "pencil"
        on_release: app.show_edit_dialog(root.phone, root.name)
    MDIconButton:
        icon: "play-circle"
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        on_release: app.fire_single(root.phone, root.name, "ON")
    MDIconButton:
        icon: "stop-circle"
        theme_text_color: "Custom"
        text_color: 1, 0.3, 0.3, 1
        on_release: app.fire_single(root.phone, root.name, "OFF")
    MDIconButton:
        icon: "trash-can-outline"
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
        spacing: "20dp"
        md_bg_color: self.theme_cls.bg_normal
        Widget:
            size_hint_y: None
            height: "50dp"
        MDIcon:
            icon: "shield-lock"
            pos_hint: {{"center_x": .5}}
            font_size: "80sp"
            theme_text_color: "Primary"
        MDLabel:
            text: "RSS CONTROL"
            halign: "center"
            font_style: "H5"
            bold: True
        MDTextField:
            id: pin_input
            hint_text: "შეიყვანეთ PIN"
            password: True
            mode: "rectangle"
            halign: "center"
            font_name_hint_text: "{USED_FONT}"
            on_text_validate: app.check_login(self.text)
        MDFillRoundFlatIconButton:
            text: "შესვლა"
            icon: "login"
            size_hint_x: .8
            pos_hint: {{"center_x": .5}}
            on_release: app.check_login(pin_input.text)
        Widget:

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
            spacing: "30dp"
            MDCard:
                id: status_card
                size_hint_y: None
                height: "150dp"
                radius: [25,]
                md_bg_color: app.theme_cls.primary_dark
                padding: "20dp"
                MDBoxLayout:
                    orientation: "vertical"
                    spacing: "10dp"
                    MDIcon:
                        id: status_icon
                        icon: "check-decagram"
                        halign: "center"
                        font_size: "35sp"
                    MDLabel:
                        id: live_node_name
                        text: "სისტემა მზად არის"
                        halign: "center"
                        font_style: "H6"
                        bold: True
                    MDLabel:
                        id: live_status_text
                        text: "მოთხოვნის მოლოდინში..."
                        halign: "center"
                        theme_text_color: "Hint"
            MDBoxLayout:
                orientation: "vertical"
                spacing: "15dp"
                MDFillRoundFlatIconButton:
                    text: "ყველას ჩართვა (ON)"
                    icon: "power"
                    size_hint: (1, None)
                    height: "60dp"
                    on_release: app.confirm_action("ON")
                MDFillRoundFlatIconButton:
                    text: "ყველას გათიშვა (OFF)"
                    icon: "power-off"
                    size_hint: (1, None)
                    height: "60dp"
                    md_bg_color: 0.8, 0.2, 0.2, 1
                    on_release: app.confirm_action("OFF")
            Widget:

<DatabaseScreen>:
    name: "database"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "ბაზა"
            left_action_items: [["arrow-left", lambda x: app.change_screen("settings")]]
            right_action_items: [["plus", lambda x: app.show_add_dialog()]]
        MDBoxLayout:
            size_hint_y: None
            height: "60dp"
            padding: ["15dp", "5dp", "15dp", "5dp"]
            MDTextField:
                id: search_field
                hint_text: "ძებნა..."
                on_text: app.refresh_ui(self.text)
                mode: "line"
                icon_left: "magnify"
                font_name_hint_text: "{USED_FONT}"
        
        RecycleView:
            id: rv
            viewclass: 'StopRow'
            RecycleBoxLayout:
                default_size: None, dp(85)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
                spacing: dp(12)
                padding: dp(15)

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
                spacing: "18dp"
                size_hint_y: None
                height: self.minimum_height
                MDLabel:
                    text: "ავტომატიზაცია"
                    bold: True
                MDTextField:
                    id: time_on
                    hint_text: "ჩართვის დრო (მაგ: 08:00)"
                    mode: "fill"
                    font_name_hint_text: "{USED_FONT}"
                MDTextField:
                    id: time_off
                    hint_text: "გამორთვის დრო (მაგ: 19:00)"
                    mode: "fill"
                    font_name_hint_text: "{USED_FONT}"
                MDBoxLayout:
                    size_hint_y: None
                    height: "50dp"
                    MDLabel:
                        text: "ავტო-რეჟიმი"
                    MDSwitch:
                        id: auto_switch
                        on_active: app.save_db_async()
                MDSeparator:
                MDFillRoundFlatIconButton:
                    text: "ავტობუსების ბაზა"
                    icon: "database-settings"
                    size_hint_x: 1
                    on_release: app.change_screen("database")
                MDSeparator:
                MDTextField:
                    id: new_pin
                    hint_text: "ახალი PIN კოდი"
                    password: True
                    mode: "fill"
                    font_name_hint_text: "{USED_FONT}"
                MDFillRoundFlatIconButton:
                    text: "პარამეტრების შენახვა"
                    icon: "content-save"
                    size_hint_x: 1
                    on_release: app.save_settings()
                MDFillRoundFlatIconButton:
                    text: "დიზაინის შეცვლა"
                    icon: "palette"
                    size_hint_x: 1
                    on_release: app.show_color_picker()
                Widget:
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

class RSSMobileApp(MDApp):
    def build(self):
        self.title = "RSS Control Pro"
        self.db = self.load_db()
        self.history = self.load_history()
        self.unit_status = self.db.get("states", {}) 
        
        self.theme_cls.theme_style = self.db.get("theme_style", "Dark")
        self.theme_cls.primary_palette = self.db.get("primary_palette", "Cyan")
        
        if USED_FONT != "Roboto":
            for style in list(self.theme_cls.font_styles.keys()):
                if style not in ["Icon", "Icons"]:
                    self.theme_cls.font_styles[style][0] = USED_FONT

        self.dia = None
        return Builder.load_string(KV)

    def on_start(self):
        if platform == 'android':
            try:
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                activity = PythonActivity.mActivity
                ActivityInfo = autoclass('android.content.pm.ActivityInfo')
                activity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_SENSOR)
            except: pass

    def check_login(self, pin):
        if str(pin) == str(self.db.get("app_pin", "1234")):
            self.root.current = "main"
        else:
            self.root.get_screen("login").ids.pin_input.error = True

    def load_db(self):
        path = get_path("system_config.dat")
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    return json.loads(base64.b64decode(f.read()).decode())
            except: pass
        return {"nums": {}, "states": {}, "on": "07:00", "off": "18:00", "active": False, "theme_style": "Dark", "primary_palette": "Cyan", "app_pin": "1234"}

    def save_db_async(self, *args):
        threading.Thread(target=self._save_db_worker, daemon=True).start()

    def _save_db_worker(self):
        try:
            path = get_path("system_config.dat")
            self.db["states"] = self.unit_status
            data = base64.b64encode(json.dumps(self.db).encode())
            with open(path, "wb") as f:
                f.write(data)
        except: pass

    def show_unit_dialog(self, title, name, phone, is_edit=False, old_phone=None):
        self.close_dia()
        c = BoxLayout(orientation='vertical', spacing="12dp", size_hint_y=None, height="160dp")
        self.ni = MDTextField(text=name, hint_text="სახელი", mode="rectangle", font_name_hint_text=USED_FONT)
        self.pi = MDTextField(text=phone, hint_text="ტელეფონი", mode="rectangle", font_name_hint_text=USED_FONT)
        c.add_widget(self.ni); c.add_widget(self.pi)
        
        btn_text = "განახლება" if is_edit else "შენახვა"
        self.dia = MDDialog(
            title=title, type="custom", content_cls=c,
            buttons=[
                MDFlatButton(text="გაუქმება", on_release=lambda x: self.close_dia()),
                MDRaisedButton(text=btn_text, on_release=lambda x: self.process_unit(is_edit, old_phone))
            ]
        )
        self.dia.open()

    def process_unit(self, is_edit, old_phone):
        if self.ni.text and self.pi.text:
            if is_edit and old_phone in self.db["nums"]:
                del self.db["nums"][old_phone]
            self.db["nums"][self.pi.text] = self.ni.text
            self.save_db_async()
            self.refresh_ui()
        self.close_dia()

    def refresh_ui(self, search_query=""):
        rv = self.root.get_screen("database").ids.rv
        nums = self.db.get("nums", {})
        q = search_query.lower()
        
        rv_data = []
        for p, n in nums.items():
            if q in n.lower() or q in p:
                state = self.unit_status.get(p, "OFF")
                color = [0, 1, 0, 1] if state == "ON" else [1, 0, 0, 1]
                rv_data.append({'name': n, 'phone': p, 'status_color': color})
        
        rv.data = rv_data

    def _send_logic(self, phone, name, cmd_type, is_batch=False):
        if not is_batch:
            Clock.schedule_once(lambda dt: self.update_status_ui(name, "იგზავნება...", [0.8, 0.5, 0, 1], "transmit"))
        
        params = {"username": API_DATA['u'], "password": API_DATA['p'], "client_id": API_DATA['c'], "service_id": API_DATA['s'], "to": phone, "text": f"1234#{cmd_type}#", "sender": API_DATA['sd']}
        success = False
        try:
            r = requests.get(API_BASE_URL, params=params, headers={"MSG_HEADER": API_DATA['h']}, timeout=8, verify=False)
            if "0000" in r.text:
                success = True
                if not is_batch:
                    Clock.schedule_once(lambda dt: self.update_status_ui(name, "წარმატებით ✅", [0, 0.4, 0.2, 1], "check-circle"))
        except: pass
        
        if success:
            self.unit_status[phone] = cmd_type
            self.save_db_async()

        entry = {"time": time.strftime("%H:%M:%S"), "name": name, "cmd": cmd_type, "icon": "check-circle" if success else "alert-circle"}
        self.history.insert(0, entry)
        self.history = self.history[:30]
        self.save_history_async()

    def save_history_async(self):
        def _save():
            try:
                with open(get_path("activity_log.json"), "w", encoding='utf-8') as f:
                    json.dump(self.history, f, ensure_ascii=False)
            except: pass
        threading.Thread(target=_save, daemon=True).start()

    def change_screen(self, name):
        self.root.current = name
        if name == "database": self.refresh_ui()
        elif name == "history": self.refresh_history_ui()
        elif name == "settings":
            s = self.root.get_screen("settings").ids
            s.time_on.text = self.db.get("on", "07:00")
            s.time_off.text = self.db.get("off", "18:00")
            s.auto_switch.active = self.db.get("active", False)

    def remove_unit(self, phone):
        if phone in self.db["nums"]:
            del self.db["nums"][phone]
            if phone in self.unit_status: del self.unit_status[phone]
            self.save_db_async()
            self.refresh_ui()

    def close_dia(self, *args):
        if self.dia: self.dia.dismiss(); self.dia = None

    def update_status_ui(self, name, text, color, icon):
        ui = self.root.get_screen("main").ids
        ui.live_node_name.text = name
        ui.live_status_text.text = text
        ui.status_card.md_bg_color = color
        ui.status_icon.icon = icon

    def fire_single(self, phone, name, cmd_type):
        self.change_screen("main")
        threading.Thread(target=self._send_logic, args=(phone, name, cmd_type), daemon=True).start()

    def confirm_action(self, cmd_type):
        self.close_dia()
        self.dia = MDDialog(
            title="დადასტურება", text=f"გსურთ ყველას {cmd_type}?",
            buttons=[MDFlatButton(text="არა", on_release=lambda x: self.close_dia()),
                     MDRaisedButton(text="დიახ", on_release=lambda x: self.run_broadcast(cmd_type))]
        )
        self.dia.open()

    def run_broadcast(self, cmd_type):
        self.close_dia()
        self.prog_bar = MDProgressBar(value=0)
        self.prog_label = MDLabel(text="მზადება...", halign="center")
        content = BoxLayout(orientation="vertical", spacing="10dp", size_hint_y=None, height="80dp")
        content.add_widget(self.prog_label); content.add_widget(self.prog_bar)
        self.dia = MDDialog(title="გაგზავნა", type="custom", content_cls=content, auto_dismiss=False)
        self.dia.open()
        threading.Thread(target=self._broadcast_logic, args=(cmd_type,), daemon=True).start()

    def _broadcast_logic(self, cmd_type):
        units = list(self.db["nums"].items())
        total = len(units)
        for index, (p, n) in enumerate(units):
            self._send_logic(p, n, cmd_type, is_batch=True)
            Clock.schedule_once(lambda dt, v=((index+1)/total)*100, m=f"გაგზავნა: {index+1}/{total}": self._update_prog_bar(v,m))
            time.sleep(0.3)
        Clock.schedule_once(lambda dt: self.close_dia())

    def _update_prog_bar(self, val, msg):
        self.prog_bar.value = val
        self.prog_label.text = msg

    def refresh_history_ui(self):
        container = self.root.get_screen("history").ids.history_list
        container.clear_widgets()
        for item in self.history:
            li = OneLineIconListItem(text=f"[{item['time']}] {item['name']} -> {item['cmd']}")
            li.add_widget(IconLeftWidget(icon=item['icon']))
            container.add_widget(li)

    def load_history(self):
        path = get_path("activity_log.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding='utf-8') as f: return json.load(f)
            except: return []
        return []

    def clear_history(self):
        self.history = []; self.refresh_history_ui()
        try: os.remove(get_path("activity_log.json"))
        except: pass

    def show_color_picker(self):
        self.close_dia()
        grid = GridLayout(cols=3, spacing="10dp", size_hint_y=None, height="150dp")
        colors = [("Cyan", [0, .8, .8, 1]), ("Amber", [1, .6, 0, 1]), ("Pink", [1, .2, .5, 1]), ("Blue", [.1, .4, .9, 1]), ("Teal", [0, .5, .4, 1]), ("Orange", [1, 0.5, 0, 1])]
        for n, c in colors:
            btn = MDIconButton(icon="circle", text_color=c, theme_text_color="Custom", icon_size="48sp")
            btn.bind(on_release=lambda x, p=n: self.update_theme(p))
            grid.add_widget(btn)
        self.dia = MDDialog(title="აირჩიე ფერი", type="custom", content_cls=grid)
        self.dia.open()

    def update_theme(self, p):
        self.theme_cls.primary_palette = p
        self.db["primary_palette"] = p
        self.save_db_async()
        self.close_dia()

    def save_settings(self):
        s = self.root.get_screen("settings").ids
        if s.new_pin.text: self.db["app_pin"] = s.new_pin.text
        self.db.update({"on": s.time_on.text, "off": s.time_off.text, "active": s.auto_switch.active})
        self.save_db_async()
        self.change_screen("main")

    def show_add_dialog(self):
        self.show_unit_dialog("დამატება", "", "")

    def show_edit_dialog(self, phone, name):
        self.show_unit_dialog("რედაქტირება", name, phone, is_edit=True, old_phone=phone)

if __name__ == "__main__":
    RSSMobileApp().run()
