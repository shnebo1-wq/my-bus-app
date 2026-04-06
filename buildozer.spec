[app]

# (str) Title of your application
title = RSS Control Center Pro

# (str) Package name
package.name = rss_commander

# (str) Package domain
package.domain = org.rss.bus

# (str) Source code where the main.py live
source.dir = .

# (list) აუცილებლად შეიყვანეთ ყველა საჭირო გაფართოება
source.include_exts = py,png,jpg,kv,atlas,ttf,json,dat

# (str) Application versioning
version = 1.0.0

# --- ჩასწორებული REQUIREMENTS ---
# ამოღებულია hostpython3 (Actions-ს თავისი აქვს) და დამატებულია certifi
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,requests,urllib3,certifi

# (str) Presplash and Icon
icon.filename = %(source.dir)s/logo.png
presplash.filename = %(source.dir)s/logo.png

# (list) Permissions
android.permissions = INTERNET, SEND_SMS, RECEIVE_SMS, READ_PHONE_STATE, READ_SMS, WAKE_LOCK, POST_NOTIFICATIONS

# --- API და NDK ფიქსი ---
android.api = 33
android.minapi = 21
# NDK 25b კარგია, მაგრამ GitHub-ზე 23b ხშირად უფრო სტაბილურია
android.ndk = 25b
android.ndk_api = 21

# (bool) Use --private data storage
android.private_storage = True

# (list) Android architectures
android.archs = arm64-v8a, armeabi-v7a

# (bool) Full screen application
fullscreen = 1

# (str) Supported orientation
orientation = portrait

# (bool) enable AndroidX support. Required for KivyMD.
android.enable_androidx = True

# (bool) Accept SDK license
android.accept_sdk_license = True

# (str) python-for-android branch
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
