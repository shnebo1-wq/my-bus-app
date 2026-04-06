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

# (list) List of inclusions using pattern matching
# source.include_patterns = assets/*,images/*.png

# (str) Application versioning
version = 1.0.0

# (list) კრიტიკული ხაზი: ბიბლიოთეკების სწორი ვერსიები
requirements = python3,hostpython3,kivy==2.3.0,kivymd==1.2.0,pillow,requests,urllib3,chardet,idna,certifi,openssl

# (str) Custom source folders for requirements
# requirements.source.kivymd = ../kivymd

# (str) Presplash and Icon (დარწმუნდით რომ ფაილები დევს GitHub-ზე)
icon.filename = %(source.dir)s/logo.png
presplash.filename = %(source.dir)s/logo.png

# (list) Permissions (საჭიროა SMS-ისთვის და ინტერნეტისთვის)
android.permissions = INTERNET, SEND_SMS, RECEIVE_SMS, READ_PHONE_STATE, READ_SMS, WAKE_LOCK, POST_NOTIFICATIONS

# (int) Target Android API (33 არის ოპტიმალური დღეს)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

# (bool) Use --private data storage
android.private_storage = True

# (list) Android architectures (ორივე საჭიროა სხვადასხვა ტელეფონისთვის)
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
# დეტალური ლოგები შეცდომების საპოვნელად
log_level = 2
warn_on_root = 1

# (str) Path to build artifacts
# build_dir = ./.buildozer

# (str) Path to bin directory
# bin_dir = ./bin
