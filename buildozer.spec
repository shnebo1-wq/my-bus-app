[app]
title = RSS Pro
package.name = rss_commander
package.domain = org.rss.bus
source.dir = .
source.include_exts = py,png,jpg,kv,ttf,json
version = 1.0.0

# კრიტიკული ბიბლიოთეკები
requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests,urllib3,certifi,pillow

# Permissions
android.permissions = INTERNET, SEND_SMS, RECEIVE_SMS, READ_PHONE_STATE, WAKE_LOCK

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.enable_androidx = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
