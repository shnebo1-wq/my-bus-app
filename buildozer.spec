[app]

# (str) Title of your application
title = RSS Control Center Pro

# (str) Package name
package.name = rss_commander

# (str) Package domain
package.domain = org.rss.bus

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (py, kv, png, ttf etc.)
source.include_exts = py,png,jpg,kv,atlas,ttf,json,dat

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
# მნიშვნელოვანი: kivymd==1.2.0 და სხვა დამოკიდებულებები
requirements = python3,hostpython3,kivy==2.3.0,kivymd==1.2.0,pillow,requests,urllib3,chardet,idna,certifi,openssl

# (str) Custom source folders for requirements (if any)
# source.include_patterns = assets/*,images/*.png

# (str) Application icon and presplash
icon.filename = %(source.dir)s/logo.png
presplash.filename = %(source.dir)s/logo.png

# (list) Permissions
# დამატებულია POST_NOTIFICATIONS Android 13-სთვის
android.permissions = INTERNET, SEND_SMS, RECEIVE_SMS, READ_PHONE_STATE, READ_SMS, WAKE_LOCK, POST_NOTIFICATIONS

# (int) Target Android API (33 is good for Play Store)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

# (bool) Use --private data storage
android.private_storage = True

# (list) Android architectures
# დავამატე armeabi-v7a სტაბილურობისთვის
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
# Log level 2 იძლევა დეტალურ ინფორმაციას შეცდომებზე
log_level = 2
warn_on_root = 1
