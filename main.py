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
from kivy.properties import StringProperty, ColorProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.app import App

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- შრიფტის რეგისტრაცია ---
FONT_NAME = "Georgian"
font_file = "bpg_arial.ttf"
if os.path.exists(font_file):
    LabelBase.register(name=FONT_NAME, fn_regular=font_file)
else:
    FONT_NAME = "Roboto"

def get_path(filename):
    try:
        base_path = App.get_running_app().user_data_dir
        if not os.path.exists(base_path): os.makedirs(base_path)
        return os.path.join(base_path, filename)
    except: return filename

API_DATA = {"u": "RSS", "p": "zLdNY8JkBi", "c": "1160", "s": "3167", "h": "FZf3eNx@ZJE", "sd": "RSS-BUS"}
API_BASE_URL = "https://bi.msg.ge/sendsms.php"

KV = f'''
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
        Widget:
            size_hint_y: None
            height: "50dp"
        MDIcon:
            icon: "shield-lock"
            pos_hint: {{"center_x": .5}}
            font_size: "80sp"
            theme_text_color: "Primary"
        MDLabel:
            text: "RSS CONTROL CENTER"
            halign: "center"
            font_name: "{FONT_NAME}"
            font_style: "H5"
            bold: True
        MDTextField:
            id: pin_input
            hint_text: "შეიყვანეთ PIN"
            font_name: "{FONT_NAME}"
            password: True
            mode: "rectangle"
            halign: "center"
            on_kv_post: app.fix_font(self)
        MDFillRoundFlatIconButton:
            text: "შესვლა"
            icon: "login"
            font_name: "{FONT_NAME}"
            size_hint_x: .8
            pos_hint: {{"center_x": .5}}
            on_release: app.check_login(pin_input.text)
        Widget:

<StopRow>:
    orientation: "horizontal"
    size_hint_y: None
    height: "90dp"
    padding: "12dp"
    spacing: "10dp"
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
            font_name: "{FONT_NAME}"
            bold: True
            font_style: "Subtitle1"
        MDLabel:
            text: root.phone
            font_name: "{FONT_NAME}"
            theme_text_color: "Hint"
            font_style: "Caption"

    MDIconButton:
        icon: "pencil-outline"
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

<MainScreen>:
    name: "main"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "RSS COMMANDER"
            font_name: "{FONT_NAME}"
            elevation: 4
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
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        opacity: app.status_opacity
                    MDLabel:
                        id: live_node_name
                        text: "სისტემა მზად არის"
                        font_name: "{FONT_NAME}"
                        halign: "center"
                        font_style: "H6"
                        bold: True
                    MDLabel:
                        id: live_status_text
                        text: "მოთხოვნის მოლოდინში..."
                        font_name: "{FONT_NAME}"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 0.9, 0.9, 0.9, 0.8
            MDBoxLayout:
                orientation: "vertical"
                spacing: "15dp"
                MDFillRoundFlatIconButton:
                    text: "ყველას ჩართვა (ON)"
                    icon: "power"
                    font_name: "{FONT_NAME}"
                    size_hint: (1, None)
                    height: "60dp"
                    on_release: app.confirm_action("ON")
                MDFillRoundFlatIconButton:
                    text: "ყველას გათიშვა (OFF)"
                    icon: "power-off"
                    font_name: "{FONT_NAME}"
                    size_hint: (1, None)
                    height: "60dp"
                    md_bg_color: 0.8, 0.2, 0.2, 1
                    on_release: app.confirm_action("OFF")
            Widget:

<SettingsScreen>:
    name: "settings"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "პარამეტრები"
            font_name: "{FONT_NAME}"
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
                    font_name: "{FONT_NAME}"
                    bold: True
                MDTextField:
                    id: time_on
                    hint_text: "ჩართვის დრო (მაგ: 07:00)"
                    text: app.db.get("on", "07:00")
                    font_name: "{FONT_NAME}"
                    mode: "fill"
                    on_kv_post: app.fix_font(self)
                MDTextField:
                    id: time_off
                    hint_text: "გამორთვის დრო (მაგ: 18:00)"
                    text: app.db.get("off", "18:00")
                    font_name: "{FONT_NAME}"
                    mode: "fill"
                    on_kv_post: app.fix_font(self)
                MDBoxLayout:
                    size_hint_y: None
                    height: "50dp"
                    MDLabel:
                        text: "ავტო-რეჟიმი"
                        font_name: "{FONT_NAME}"
                    MDSwitch:
                        id: auto_switch
                        active: app.db.get("active", False)
                        on_active: app.save_db()
                MDSeparator:
                MDFillRoundFlatIconButton:
                    text: "ავტობუსების ბაზა"
                    icon: "database-settings"
                    font_name: "{FONT_NAME}"
                    size_hint_x: 1
                    on_release: app.change_screen("database")
                MDSeparator:
                MDTextField:
                    id: new_pin
                    hint_text: "ახალი PIN კოდი"
                    password: True
                    font_name: "{FONT_NAME}"
                    mode: "fill"
                    on_kv_post: app.fix_font(self)
                MDFillRoundFlatIconButton:
                    text: "PIN-ის განახლება"
                    icon: "key-variant"
                    font_name: "{FONT_NAME}"
                    size_hint_x: 1
                    on_release: app.update_pin(new_pin.text)
                MDFillRoundFlatIconButton:
                    text: "დიზაინის შეცვლა"
                    icon: "palette"
                    font_name: "{FONT_NAME}"
                    size_hint_x: 1
                    on_release: app.show_color_picker()
                Widget:

<DatabaseScreen>:
    name: "database"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "ბაზა"
            font_name: "{FONT_NAME}"
            left_action_items: [["arrow-left", lambda x: app.change_screen("settings")]]
            right_action_items: [["plus", lambda x: app.show_add_dialog()]]
        MDBoxLayout:
            size_hint_y: None
            height: "60dp"
            padding: ["15dp", "5dp", "15dp", "5dp"]
            MDTextField:
                id: search_field
                hint_text: "ძებნა..."
                font_name: "{FONT_NAME}"
                on_text: app.refresh_ui(self.text)
                mode: "line"
                icon_left: "magnify"
                on_kv_post: app.fix_font(self)
        ScrollView:
            MDBoxLayout:
                id: unit_list
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: "15dp"
                spacing: "12dp"

<HistoryScreen>:
    name: "history"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "ისტორია"
            font_name: "{FONT_NAME}"
            left_action_items: [["arrow-left", lambda x: app.change_screen("main")]]
            right_action_items: [["delete-sweep", lambda x: app.clear_history()]]
        ScrollView:
            MDList:
                id: history_list
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
    status_opacity = NumericProperty(1)

    def on_start(self):
        # ავტომატიზაციის ძრავის ჩართვა აპლიკაციის დაწყებისას
        threading.Thread(target=self.auto_engine, daemon=True).start()

    def build(self):
        self.db = self.load_db()
        self.history = self.load_history()
        self.theme_cls.theme_style = self.db.get("theme_style", "Dark")
        self.theme_cls.primary_palette = self.db.get("primary_palette", "Cyan")
        self.dia = None
        self.is_broadcasting = False
        
        if FONT_NAME == "Georgian":
            for style in list(self.theme_cls.font_styles.keys()):
                if style not in ["Icon", "Icons"]:
                    self.theme_cls.font_styles[style][0] = FONT_NAME
        
        return Builder.load_string(KV)

    def fix_font(self, field):
        field.font_name = FONT_NAME
        field.font_name_hint_text = FONT_NAME
        if hasattr(field, "_hint_lbl"): field._hint_lbl.font_name = FONT_NAME

    def auto_engine(self):
        while True:
            try:
                if self.db.get("active") and not self.is_broadcasting:
                    current_time = time.strftime("%H:%M")
                    if current_time == self.db.get("on"):
                        self.run_broadcast_silent("ON")
                        time.sleep(65) # რომ ერთ წუთში ორჯერ არ გააგზავნოს
                    elif current_time == self.db.get("off"):
                        self.run_broadcast_silent("OFF")
                        time.sleep(65)
            except Exception as e:
                print(f"Auto Engine Error: {e}")
            time.sleep(30)

    def run_broadcast_silent(self, cmd_type):
        threading.Thread(target=self._broadcast_logic_silent, args=(cmd_type,), daemon=True).start()

    def _broadcast_logic_silent(self, cmd_type):
        self.is_broadcasting = True
        units = list(self.db["nums"].items())
        for p, n in units:
            self._send_logic(p, n, cmd_type, is_batch=True)
            time.sleep(0.5)
        self.is_broadcasting = False

    def load_db(self):
        path = get_path("system_config.dat")
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    return json.loads(base64.b64decode(f.read()).decode())
            except: pass
        return {"nums": {}, "on": "07:00", "off": "18:00", "active": False, "statuses": {}, "theme_style": "Dark", "primary_palette": "Cyan", "app_pin": "1234"}

    def save_db(self, *args):
        try:
            path = get_path("system_config.dat")
            try:
                s = self.root.get_screen("settings").ids
                self.db.update({"on": s.time_on.text, "off": s.time_off.text, "active": s.auto_switch.active})
            except: pass
            
            self.db.update({"theme_style": self.theme_cls.theme_style, "primary_palette": self.theme_cls.primary_palette})
            with open(path, "wb") as f:
                f.write(base64.b64encode(json.dumps(self.db).encode()))
        except: pass

    def refresh_ui(self, search_query=""):
        try:
            container = self.root.get_screen("database").ids.unit_list
            container.clear_widgets()
            nums = self.db.get("nums", {})
            stats = self.db.get("statuses", {})
            q = search_query.lower()
            for p, n in nums.items():
                if q in n.lower() or q in p:
                    current_stat = stats.get(p, -1)
                    color = [0.2, 0.8, 0.2, 1] if current_stat == 1 else ([0.9, 0.2, 0.2, 1] if current_stat == 0 else [0.5, 0.5, 0.5, 1])
                    container.add_widget(StopRow(name=n, phone=p, status_color=color))
        except: pass

    def show_edit_dialog(self, phone, old_name):
        self.close_dia()
        c = BoxLayout(orientation='vertical', spacing="12dp", size_hint_y=None, height="160dp")
        self.ni = MDTextField(text=old_name, hint_text="ახალი სახელი", mode="rectangle")
        self.pi = MDTextField(text=phone, hint_text="ნომერი", mode="rectangle", readonly=True)
        self.fix_font(self.ni); self.fix_font(self.pi)
        c.add_widget(self.ni); c.add_widget(self.pi)
        self.dia = MDDialog(
            title="რედაქტირება", type="custom", content_cls=c,
            buttons=[
                MDFlatButton(text="გაუქმება", font_name=FONT_NAME, on_release=lambda x: self.close_dia()),
                MDRaisedButton(text="შენახვა", font_name=FONT_NAME, on_release=lambda x: self.save_edit(phone))
            ]
        )
        self.dia.ids.title.font_name = FONT_NAME
        self.dia.open()

    def save_edit(self, phone):
        if self.ni.text:
            self.db["nums"][phone] = self.ni.text
            self.save_db(); self.refresh_ui()
        self.close_dia()

    def show_add_dialog(self):
        self.close_dia()
        c = BoxLayout(orientation='vertical', spacing="12dp", size_hint_y=None, height="160dp")
        self.ni = MDTextField(hint_text="სახელი", mode="rectangle")
        self.pi = MDTextField(hint_text="ნომერი", mode="rectangle")
        self.fix_font(self.ni); self.fix_font(self.pi)
        c.add_widget(self.ni); c.add_widget(self.pi)
        self.dia = MDDialog(
            title="დამატება", type="custom", content_cls=c,
            buttons=[
                MDFlatButton(text="გაუქმება", font_name=FONT_NAME, on_release=lambda x: self.close_dia()),
                MDRaisedButton(text="შენახვა", font_name=FONT_NAME, on_release=self.add_unit)
            ]
        )
        self.dia.ids.title.font_name = FONT_NAME
        self.dia.open()

    def add_unit(self, *args):
        if self.ni.text and self.pi.text:
            self.db["nums"][self.pi.text] = self.ni.text
            self.save_db(); self.refresh_ui()
        self.close_dia()

    def remove_unit(self, phone):
        if phone in self.db["nums"]:
            del self.db["nums"][phone]
            if phone in self.db["statuses"]: del self.db["statuses"][phone]
            self.save_db(); self.refresh_ui()

    def fire_single(self, phone, name, cmd_type):
        self.change_screen("main")
        threading.Thread(target=self._send_logic, args=(phone, name, cmd_type), daemon=True).start()

    def _send_logic(self, phone, name, cmd_type, is_batch=False):
        if not is_batch:
            Clock.schedule_once(lambda dt: self.update_status_ui(name, "აგზავნის...", [0.8, 0.5, 0, 1], "transmit"))
        
        pwd = self.db.get("app_pin", "1234")
        params = {"username": API_DATA['u'], "password": API_DATA['p'], "client_id": API_DATA['c'], "service_id": API_DATA['s'], "to": phone, "text": f"{pwd}#{cmd_type}#", "sender": API_DATA['sd']}
        icon = "alert-circle"
        try:
            r = requests.get(API_BASE_URL, params=params, headers={"MSG_HEADER": API_DATA['h']}, timeout=10, verify=False)
            if "0000" in r.text:
                self.db["statuses"][phone] = 1 if cmd_type == "ON" else 0
                self.save_db()
                if not is_batch:
                    Clock.schedule_once(lambda dt: self.update_status_ui(name, "გაიგზავნა✅", [0, 0.4, 0.2, 1], "check-circle"))
                icon = "check-circle"
                Clock.schedule_once(lambda dt: self.refresh_ui())
        except: pass
        
        entry = {"time": time.strftime("%H:%M:%S"), "name": name, "cmd": cmd_type, "icon": icon}
        self.history.insert(0, entry); self.history = self.history[:30]
        self.save_history()

    def update_status_ui(self, name, text, color, icon):
        try:
            ui = self.root.get_screen("main").ids
            ui.live_node_name.text = name
            ui.live_status_text.text = text
            ui.status_card.md_bg_color = color
            ui.status_icon.icon = icon
        except: pass

    def confirm_action(self, cmd_type):
        self.close_dia()
        self.dia = MDDialog(
            title="დადასტურება", text=f"გსურთ ყველას {cmd_type}?", font_name=FONT_NAME,
            buttons=[MDFlatButton(text="არა", font_name=FONT_NAME, on_release=lambda x: self.close_dia()),
                     MDRaisedButton(text="დიახ", font_name=FONT_NAME, on_release=lambda x: self.run_broadcast(cmd_type))]
        )
        self.dia.ids.title.font_name = FONT_NAME
        self.dia.open()

    def run_broadcast(self, cmd_type):
        self.close_dia()
        self.prog_bar = MDProgressBar(value=0)
        self.prog_label = MDLabel(text="ემზადება...", font_name=FONT_NAME, halign="center")
        content = BoxLayout(orientation="vertical", spacing="10dp", size_hint_y=None, height="80dp")
        content.add_widget(self.prog_label); content.add_widget(self.prog_bar)
        self.dia = MDDialog(title="გაგზავნა", type="custom", content_cls=content, auto_dismiss=False)
        self.dia.ids.title.font_name = FONT_NAME
        self.dia.open()
        threading.Thread(target=self._broadcast_logic, args=(cmd_type,), daemon=True).start()

    def _broadcast_logic(self, cmd_type):
        self.is_broadcasting = True
        units = list(self.db["nums"].items())
        total = len(units)
        for index, (p, n) in enumerate(units):
            progress = ((index + 1) / total) * 100
            Clock.schedule_once(lambda dt, v=progress, i=index+1, t=total: self._update_prog_bar(v, f"იგზავნება: {i} / {t}"))
            self._send_logic(p, n, cmd_type, is_batch=True)
            time.sleep(0.5)
        Clock.schedule_once(lambda dt: self.close_dia())
        self.is_broadcasting = False

    def _update_prog_bar(self, val, msg):
        try:
            self.prog_bar.value = val
            self.prog_label.text = msg
        except: pass

    def check_login(self, pin):
        if pin == self.db.get("app_pin", "1234"): self.root.current = "main"
        else: self.root.get_screen("login").ids.pin_input.error = True

    def change_screen(self, name):
        self.root.current = name
        if name == "database": self.refresh_ui()
        elif name == "history": self.refresh_history_ui()

    def refresh_history_ui(self):
        try:
            container = self.root.get_screen("history").ids.history_list
            container.clear_widgets()
            for item in self.history:
                li = OneLineIconListItem(text=f"[{item['time']}] {item['name']} -> {item['cmd']}", font_name=FONT_NAME)
                li.add_widget(IconLeftWidget(icon=item['icon']))
                container.add_widget(li)
        except: pass

    def save_history(self):
        try:
            with open(get_path("activity_log.json"), "w", encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False)
        except: pass

    def load_history(self):
        path = get_path("activity_log.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding='utf-8') as f: return json.load(f)
            except: return []
        return []

    def close_dia(self, *args):
        if self.dia: self.dia.dismiss(); self.dia = None

    def show_color_picker(self):
        self.close_dia()
        grid = GridLayout(cols=3, spacing="10dp", size_hint_y=None, height="150dp")
        colors = [("Cyan", [0, .8, .8, 1]), ("Amber", [1, .6, 0, 1]), ("Pink", [1, .2, .5, 1]), 
                  ("Blue", [.1, .4, .9, 1]), ("Teal", [0, .5, .4, 1]), ("Orange", [1, 0.5, 0, 1])]
        for n, c in colors:
            btn = MDIconButton(icon="circle", text_color=c, theme_text_color="Custom", icon_size="48sp")
            btn.bind(on_release=lambda x, p=n: self.update_theme(p))
            grid.add_widget(btn)
        self.dia = MDDialog(title="ფერები", type="custom", content_cls=grid)
        self.dia.ids.title.font_name = FONT_NAME
        self.dia.open()

    def update_theme(self, p):
        self.theme_cls.primary_palette = p; self.save_db(); self.close_dia()

    def clear_history(self):
        self.history = []; self.refresh_history_ui()
        try: os.remove(get_path("activity_log.json"))
        except: pass

    def update_pin(self, new_pin):
        if len(new_pin) >= 4:
            self.db["app_pin"] = new_pin; self.save_db()
            self.root.get_screen("settings").ids.new_pin.text = ""

if __name__ == "__main__":
    RSSMobileApp().run()
