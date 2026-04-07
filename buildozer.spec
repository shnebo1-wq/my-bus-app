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
requirements = python3,kivy,kivymd,requests,urllib3,certifi

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
# 'all' ნიშნავს სრულ ავტო-როტაციას ყველა მხარეს
orientation = all

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

# (bool) OK for Android SDK license
android.accept_sdk_license = True

# (str) The Android arch to build for.
android.archs = arm64-v8a

# (bool) enables Androidx explicitely.
android.enable_androidx = True

# --- ოპტიმიზაცია GitHub-ისთვის ---
android.no_byte_compile_python_optimization = 1

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1

# (str) Path to build artifacts
bin_dir = ./bin
