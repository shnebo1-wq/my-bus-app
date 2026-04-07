[app]

# (str) Title of your application
title = RSS Control Pro

# (str) Package name
package.name = rss_commander

# (str) Package domain (needed for android packaging)
package.domain = org.rss.bus

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,ttf,json,dat

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# დამატებულია Kivy და KivyMD ვერსიების გარეშე სტაბილურობისთვის
requirements = python3,kivy,kivymd,requests,urllib3,certifi

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
# ჩართულია 'sensor' ავტო-როტაციისთვის
orientation = sensor

# (list) Permissions
android.permissions = INTERNET, SEND_SMS, RECEIVE_SMS, READ_PHONE_STATE, WAKE_LOCK, READ_SMS

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded)
android.accept_sdk_license = True

# (str) The Android arch to build for. 
# GitHub Actions-ისთვის მხოლოდ ერთი (arm64-v8a) ყველაზე სწრაფია
android.archs = arm64-v8a

# (bool) enables Androidx explicitely.
android.enable_androidx = True

# (str
