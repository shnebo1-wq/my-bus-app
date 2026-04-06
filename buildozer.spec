[app]

# (str) Title of your application
title = RSS Control Center Pro

# (str) Package name
package.name = rss_commander

# (str) Package domain (needed for android packaging)
package.domain = org.rss.bus

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include ( py, kv, ttf - აუცილებელია ფონტისთვის)
source.include_exts = py,png,jpg,kv,atlas,ttf,json,dat

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
# აქ დამატებულია openssl და requests-ის დამხმარე ბიბლიოთეკები
requirements = python3, kivy==2.3.0, kivymd, pillow, openssl, requests, urllib3, chardet, idna, certifi, sh

# (str) Custom icon (შეცვალეთ თქვენი ფაილის სახელით)
icon.filename = %(source.dir)s/logo.png

# (str) Presplash (ჩატვირთვის ეკრანი)
presplash.filename = %(source.dir)s/logo.png

# (list) Permissions - ინტერნეტი და SMS
android.permissions = INTERNET, SEND_SMS, RECEIVE_SMS, READ_PHONE_STATE, READ_SMS, WAKE_LOCK

# (int) Target Android API
android.api = 33

# (int) Minimum API
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (int) Android NDK API
android.ndk_api = 21

# (bool) Use --private data storage
android.private_storage = True

# (list) Android architectures (arm64-v8a ყველაზე სტანდარტულია დღეს)
android.archs = arm64-v8a

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

# (int) Log level (2 ნიშნავს სრულ დეტალებს ერორების საპოვნელად)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
