[app]
title = RSS Control Center Pro
package.name = rss_commander
package.domain = org.rss.bus
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json,dat
version = 1.0.0

# --- ოპტიმიზირებული REQUIREMENTS ---
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,requests,urllib3,certifi

# --- დროებით დააკომენტარე ეს ხაზები (ტესტისთვის) ---
# თუ ბილდი გაიარა, მერე სათითაოდ ჩავრთავთ
# icon.filename = %(source.dir)s/logo.png
# presplash.filename = %(source.dir)s/logo.png

android.permissions = INTERNET, SEND_SMS, RECEIVE_SMS, READ_PHONE_STATE, READ_SMS, WAKE_LOCK, POST_NOTIFICATIONS

android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.private_storage = True
android.archs = arm64-v8a, armeabi-v7a
fullscreen = 1
orientation = portrait
android.enable_androidx = True
android.accept_sdk_license = True
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
