[app]

# (str) Title of your application
title = RSS Control Center Pro

# (str) Package name
package.name = rss_commander

# (str) Package domain (needed for android packaging)
package.domain = org.rss.bus

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let's empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf,json,dat

# (list) List of inclusions using pattern matching
# source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let's empty to exclude nothing)
# source.exclude_exts = spec

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# დამატებულია: openssl (HTTPS-ისთვის), certifi/idna/urllib3 (requests-ისთვის)
requirements = python3, kivy==2.3.0, kivymd, pillow, openssl, requests, urllib3, chardet, idna, certifi, sh

# (str) Custom source folders for requirements
# packagelist.vendor = 

# (list) Permissions
android.permissions = INTERNET, SEND_SMS, RECEIVE_SMS, READ_PHONE_STATE, READ_SMS, WAKE_LOCK

# (list) features required by the app
# android.features = android.hardware.telephony

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
# android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (list) Android architectures to build for
android.archs = arm64-v8a

# (bool) Full screen application
fullscreen = 1

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be allowed to exit when pressing the back button.
# android.allow_backup = True

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# android.arch = arm64-v8a

# (bool) enable AndroidX support. Required for KivyMD.
android.enable_androidx = True

# (bool) Accept SDK license
android.accept_sdk_license = True

# (str) python-for-android branch to use
p4a.branch = master

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = NO, 1 = YES)
warn_on_root = 1

# (str) Path to build artifact storage, default is to use binaries/ within the project
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab location)
# bin_dir = ./bin
