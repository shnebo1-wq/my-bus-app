[app]
# (str) Title of your application
title = RSS Control Pro

# (str) Package name
package.name = rss_commander

# (str) Package domain
package.domain = org.rss.bus

# (str) Source code where the main.py live
source.dir = .

# (list) გამოსაყენებელი ფაილების გაფართოებები
source.include_exts = py,png,jpg,kv,ttf,json,dat

# (str) Application versioning
version = 1.0.0

# --- კრიტიკული ფიქსი REQUIREMENTS-ში ---
# pillow==9.5.0 არის ყველაზე სტაბილური ანდროიდისთვის
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow==9.5.0,requests,urllib3,certifi

# (list) Permissions
android.permissions = INTERNET, SEND_SMS, RECEIVE_SMS, READ_PHONE_STATE, WAKE_LOCK, POST_NOTIFICATIONS

# --- Android Settings ---
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.private_storage = True

# (list) არქიტექტურები (ორივე საჭიროა)
android.archs = arm64-v8a, armeabi-v7a

# (bool) Full screen
fullscreen = 1

# (str) Orientation
orientation = portrait

# (bool) AndroidX support - აუცილებელია KivyMD-სთვის
android.enable_androidx = True

# (bool) Accept SDK license
android.accept_sdk_license = True

# (str) python-for-android branch
p4a.branch = master

[buildozer]
# დეტალური ლოგები
log_level = 2
warn_on_root = 1
