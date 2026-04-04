import json, os, base64, threading, time, requests, urllib3
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty, ColorProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- შრიფტის რეგისტრაცია ---
FONT_NAME = "Georgian"
font_file = "bpg_arial.ttf"
if os.path.exists(font_file):
    LabelBase.register(name=FONT_NAME, fn_regular=font_file)
else: 
    FONT_NAME = "Roboto"

DB_FILE = "system_config.dat"
LOG_FILE = "activity_log.json"
API_DATA = {"u": "RSS", "p": "zLdNY8JkBi", "c": "1160", "s": "3167", "h": "FZf3eNx@ZJE", "sd": "RSS-BUS"}
API_BASE_URL = "https://bi.msg.ge/sendsms.php"

KV = f'''
ScreenManager:
    MainScreen:
    SettingsScreen:
    DatabaseScreen:
    HistoryScreen:

<StopRow>:
    orientation: "horizontal"
    size_hint_y: None
    height: "80dp"
    padding: "10dp"
    spacing: "12dp"
    canvas.before:
        Color:
            rgba: (0.12, 0.12, 0.12, 1) if app.theme_cls.theme_style == "Dark" else (0.95, 0.95, 0.95, 1)
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [18,]
    
    BoxLayout:
        size_hint: None, None
        size: "12dp", "12dp"
        pos_hint: {{"center_y": .5}}
        canvas:
            Color:
                rgba: root.status_color
            Ellipse:
                size: self.size
                pos: self.pos

    MDBoxLayout:
        orientation: "vertical"
        MDLabel:
            text: root.name
            font_name: "{FONT_NAME}"
            bold: True
        MDLabel:
            text: root.phone
            theme_text_color: "Hint"
            font_style: "Caption"

    MDIconButton:
        icon: "play-circle-outline"
        on_release: app.fire_single(root.phone, root.name, "ON")
    MDIconButton:
        icon: "stop-circle-outline"
        theme_text_color: "Custom"
        text_color: 1, 0.3, 0.3, 1
        on_release: app.fire_single(root.phone, root.name, "OFF")
    MDIconButton:
        icon: "pencil-outline"
        on_release: app.show_edit_dialog(root.phone, root.name)
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
            right_action_items: [["history", lambda x: app.change_screen("history")], ["cog", lambda x: app.change_screen("settings")]]
        MDBoxLayout:
            orientation: "vertical"
            padding: "20dp"
            spacing: "20dp"
            MDCard:
                id: status_card
                size_hint_y: None
                height: "130dp"
                radius: [22,]
                padding: "20dp"
                MDBoxLayout:
                    orientation: "vertical"
                    MDLabel:
                        id: live_node_name
                        text: "სისტემა მზად არის"
                        font_name: "{FONT_NAME}"
                        halign: "center"
                    MDLabel:
                        id: live_status_text
                        text: "მოთხოვნის მოლოდინში..."
                        font_name: "{FONT_NAME}"
                        halign: "center"
                        theme_text_color: "Hint"
            MDRaisedButton:
                text: "ყველას ჩართვა (ON)"
                font_name: "{FONT_NAME}"
                size_hint_x: 1
                on_release: app.confirm_action("ON")
            MDRaisedButton:
                text: "ყველას გათიშვა (OFF)"
                font_name: "{FONT_NAME}"
                size_hint_x: 1
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
        MDBoxLayout:
            orientation: "vertical"
            padding: "20dp"
            spacing: "15dp"
            MDTextField:
                id: time_on
                hint_text: "ჩართვის დრო"
                font_name: "{FONT_NAME}"
                font_name_hint_text: "{FONT_NAME}"
                mode: "rectangle"
            MDTextField:
                id: time_off
                hint_text: "გამორთვის დრო"
                font_name: "{FONT_NAME}"
                font_name_hint_text: "{FONT_NAME}"
                mode: "rectangle"
            MDBoxLayout:
                size_hint_y: None
                height: "50dp"
                MDLabel:
                    text: "ავტო-რეჟიმი"
                    font_name: "{FONT_NAME}"
                MDSwitch:
                    id: auto_switch
                    on_active: app.save_db()
            MDRaisedButton:
                text: "ავტობუსების ბაზა"
                font_name: "{FONT_NAME}"
                size_hint_x: 1
                on_release: app.change_screen("database")
            MDRaisedButton:
                text: "დიზაინის შეცვლა"
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
        ScrollView:
            MDBoxLayout:
                id: unit_list
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: "15dp"
                spacing: "10dp"

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
    status_color = ColorProperty([0.4, 0.4, 0.4, 1])

class MainScreen(Screen): pass
class SettingsScreen(Screen): pass
class DatabaseScreen(Screen): pass
class HistoryScreen(Screen): pass

class RSSMobileApp(MDApp):
    def build(self):
        self.db = self.load_db()
        self.history = self.load_history()
        self.theme_cls.theme_style = self.db.get("theme_style", "Dark")
        self.theme_cls.primary_palette = self.db.get("primary_palette", "Cyan")
        self.dia = None
        
        if FONT_NAME == "Georgian":
            for style in list(self.theme_cls.font_styles.keys()):
                if style not in ["Icon", "Icons"]:
                    self.theme_cls.font_styles[style][0] = FONT_NAME
        
        return Builder.load_string(KV)

    def on_start(self):
        s = self.root.get_screen("settings").ids
        s.time_on.text = self.db.get("on", "07:00")
        s.time_off.text = self.db.get("off", "18:00")
        s.auto_switch.active = self.db.get("active", False)
        self.refresh_ui()
        threading.Thread(target=self.auto_engine, daemon=True).start()

    def load_db(self):
        if os.path.exists(DB_FILE):
            try:
                with open(DB_FILE, "rb") as f:
                    return json.loads(base64.b64decode(f.read()).decode())
            except: pass
        return {"nums": {}, "on": "07:00", "off": "18:00", "active": False, "statuses": {}, "theme_style": "Dark", "primary_palette": "Cyan"}

    def save_db(self, *args):
        try:
            s = self.root.get_screen("settings").ids
            self.db.update({"on": s.time_on.text, "off": s.time_off.text, "active": s.auto_switch.active,
                           "theme_style": self.theme_cls.theme_style, "primary_palette": self.theme_cls.primary_palette})
            with open(DB_FILE, "wb") as f:
                f.write(base64.b64encode(json.dumps(self.db).encode()))
        except: pass

    def load_history(self):
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, "r", encoding='utf-8') as f: return json.load(f)
            except: return []
        return []

    def change_screen(self, name):
        self.root.current = name
        if name == "database": self.refresh_ui()
        elif name == "history": self.refresh_history_ui()

    def refresh_ui(self):
        container = self.root.get_screen("database").ids.unit_list
        container.clear_widgets()
        nums = self.db.get("nums", {})
        stats = self.db.get("statuses", {})
        for p, n in nums.items():
            container.add_widget(StopRow(name=n, phone=p, status_color=stats.get(p, [0.4, 0.4, 0.4, 1])))

    def refresh_history_ui(self):
        container = self.root.get_screen("history").ids.history_list
        container.clear_widgets()
        for item in self.history:
            li = OneLineIconListItem(text=f"[{item['time']}] {item['name']} -> {item['cmd']}")
            li.add_widget(IconLeftWidget(icon=item['icon']))
            container.add_widget(li)

    def close_dia(self, *args):
        if self.dia:
            self.dia.dismiss()
            self.dia = None

    def confirm_action(self, cmd_type):
        self.close_dia()
        self.dia = MDDialog(
            title="დადასტურება",
            text=f"გსურთ ყველას {cmd_type}?",
            buttons=[
                MDFlatButton(text="არა", font_name=FONT_NAME, on_release=lambda x: self.close_dia()),
                MDRaisedButton(text="დიახ", font_name=FONT_NAME, on_release=lambda x: self.run_broadcast(cmd_type))
            ]
        )
        self.dia.open()

    def run_broadcast(self, cmd_type):
        self.close_dia()
        threading.Thread(target=self._broadcast_logic, args=(cmd_type,), daemon=True).start()

    def _broadcast_logic(self, cmd_type):
        for p, n in list(self.db["nums"].items()):
            self._send_logic(p, n, cmd_type)
            time.sleep(1.2)

    def fire_single(self, phone, name, cmd_type):
        self.change_screen("main")
        threading.Thread(target=self._send_logic, args=(phone, name, cmd_type), daemon=True).start()

    def _send_logic(self, phone, name, cmd_type):
        Clock.schedule_once(lambda dt: self.update_status_ui(name, "აგზავნის...", [0.8, 0.5, 0, 1]))
        pwd = self.db.get('pwd', '1234')
        params = {"username": API_DATA['u'], "password": API_DATA['p'], "client_id": API_DATA['c'], 
                  "service_id": API_DATA['s'], "to": phone, "text": f"{pwd}#{cmd_type}#", "sender": API_DATA['sd']}
        icon = "alert-circle"
        try:
            r = requests.get(API_BASE_URL, params=params, headers={"MSG_HEADER": API_DATA['h']}, timeout=7, verify=False)
            if "0000" in r.text:
                Clock.schedule_once(lambda dt: self.update_status_ui(name, "გაიგზავნა ✅", [0, 0.4, 0.2, 1]))
                self.db.setdefault("statuses", {})[phone] = [0, 1, 0, 1] if cmd_type == "ON" else [1, 0, 0, 1]
                icon = "check-circle"
                self.save_db()
            else: Clock.schedule_once(lambda dt: self.update_status_ui(name, "შეცდომა ❌", [0.7, 0.1, 0.1, 1]))
        except: Clock.schedule_once(lambda dt: self.update_status_ui(name, "ხარვეზი ⚠️", [0.5, 0, 0, 1]))
        
        entry = {"time": time.strftime("%H:%M:%S"), "name": name, "cmd": cmd_type, "icon": icon}
        self.history.insert(0, entry)
        self.history = self.history[:30]
        with open(LOG_FILE, "w", encoding='utf-8') as f: json.dump(self.history, f, ensure_ascii=False)

    def update_status_ui(self, name, text, color):
        ui = self.root.get_screen("main").ids
        ui.live_node_name.text = name
        ui.live_status_text.text = text
        ui.status_card.md_bg_color = color

    def auto_engine(self):
        while True:
            if self.db.get("active"):
                t = time.strftime("%H:%M")
                if t == self.db.get("on"): self.run_broadcast("ON"); time.sleep(65)
                if t == self.db.get("off"): self.run_broadcast("OFF"); time.sleep(65)
            time.sleep(30)

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
        self.dia.open()

    def update_theme(self, p):
        self.theme_cls.primary_palette = p
        self.save_db()
        self.close_dia()

    # --- აი აქ არის ცვლილება ---
    def show_add_dialog(self):
        self.close_dia()
        c = BoxLayout(orientation='vertical', spacing="5dp", size_hint_y=None, height="180dp")
        
        # სახელი
        c.add_widget(MDLabel(text="სახელი", font_name=FONT_NAME, size_hint_y=None, height="20dp", theme_text_color="Hint"))
        self.ni = MDTextField(font_name=FONT_NAME, mode="line")
        c.add_widget(self.ni)
        
        # ნომერი
        c.add_widget(MDLabel(text="ნომერი", font_name=FONT_NAME, size_hint_y=None, height="20dp", theme_text_color="Hint"))
        self.pi = MDTextField(font_name=FONT_NAME, mode="line")
        c.add_widget(self.pi)
        
        self.dia = MDDialog(
            title="დამატება", 
            type="custom", 
            content_cls=c,
            buttons=[MDRaisedButton(text="შენახვა", font_name=FONT_NAME, on_release=self.add_unit)]
        )
        self.dia.open()

    def show_edit_dialog(self, phone, name):
        self.close_dia()
        c = BoxLayout(orientation='vertical', spacing="5dp", size_hint_y=None, height="100dp")
        
        c.add_widget(MDLabel(text="სახელი", font_name=FONT_NAME, size_hint_y=None, height="20dp", theme_text_color="Hint"))
        self.edit_name = MDTextField(text=name, font_name=FONT_NAME, mode="line")
        c.add_widget(self.edit_name)
        
        self.dia = MDDialog(
            title=f"რედაქტირება: {phone}", 
            type="custom", 
            content_cls=c,
            buttons=[MDRaisedButton(text="შენახვა", font_name=FONT_NAME, on_release=lambda x: self.update_unit(phone))]
        )
        self.dia.open()
    # ---------------------------

    def add_unit(self, *args):
        if self.ni.text and self.pi.text:
            self.db["nums"][self.pi.text] = self.ni.text
            self.save_db(); self.refresh_ui()
        self.close_dia()

    def update_unit(self, phone):
        self.db["nums"][phone] = self.edit_name.text
        self.save_db(); self.refresh_ui()
        self.close_dia()

    def remove_unit(self, phone):
        if phone in self.db["nums"]:
            del self.db["nums"][phone]
            self.save_db(); self.refresh_ui()

    def clear_history(self):
        self.history = []
        if os.path.exists(LOG_FILE): os.remove(LOG_FILE)
        self.refresh_history_ui()

if __name__ == "__main__":
    RSSMobileApp().run()