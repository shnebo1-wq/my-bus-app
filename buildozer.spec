[app]
# (str) აპლიკაციის სახელი
title = RSS Control Center Pro

# (str) პაკეტის სახელი
package.name = rss_commander

# (str) პაკეტის დომენი
package.domain = org.rss.bus

# (str) წყაროს საქაღალდე
source.dir = .

# (list) ჩასართავი ფაილები
source.include_exts = py,png,jpg,kv,atlas,ttf

# (str) ვერსია
version = 1.0.0

# (list) აუცილებელი ბიბლიოთეკები (დამატებულია openssl, requests და sh სტაბილურობისთვის)
requirements = python3,kivy==2.3.0,kivymd,pillow,openssl,requests,sh

# (list) ნებართვები (დამატებულია SMS-ის სრული მხარდაჭერა)
android.permissions = INTERNET, SEND_SMS, RECEIVE_SMS, READ_PHONE_STATE, READ_SMS, WAKE_LOCK

# (int) Android API-ს პარამეტრები (API 33 არის სტანდარტი)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

# (list) არქიტექტურა
android.archs = arm64-v8a, armeabi-v7a

# (bool) ეკრანის პარამეტრები
fullscreen = 1
orientation = portrait

# (bool) ლიცენზიის ავტომატური თანხმობა
android.accept_sdk_license = True

# (str) აპლიკაციის თემა
android.apptheme = "@android:style/Theme.NoTitleBar"

# (bool) AndroidX მხარდაჭერა (KivyMD-სთვის აუცილებელია)
android.enable_androidx = True

# (str) P4A ბრენჩი
p4a.branch = master

[buildozer]
# (int) ლოგის დონე (2 = დეტალური)
log_level = 2

# (int) გაფრთხილება root-ზე
warn_on_root = 1
