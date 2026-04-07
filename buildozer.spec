[app]
title = RSS Control Pro
package.name = rss_commander
package.domain = org.rss.bus
source.dir = .
source.include_exts = py,png,jpg,kv,ttf,json,dat
version = 1.0.0

requirements = python3,kivy,kivymd,requests,urllib3,certifi

android.permissions = INTERNET, SEND_SMS, RECEIVE_SMS, READ_PHONE_STATE, WAKE_LOCK, READ_SMS
android.api = 33
android.minapi = 21
android.ndk = 25b
android.jdk = 17
android.private_storage = True
android.enable_androidx = True
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
