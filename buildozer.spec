[app]
# (str) აპლიკაციის სახელი
title = RSS Control Center Pro

# (str) პაკეტის სახელი (უნდა იყოს პატარა ასოებით და ქვედა ტირეებით)
package.name = rss_commander

# (str) პაკეტის დომენი
package.domain = org.rss.bus

# (str) წყაროს საქაღალდე
source.dir = .

# (list) ფაილის გაფართოებები, რომლებიც უნდა შევიდეს APK-ში
source.include_exts = py,png,jpg,kv,atlas,ttf

# (str) ვერსია
version = 1.0.0

# (list) აუცილებელი ბიბლიოთეკები (აქ დავამატე openssl და sh, რაც SMS-ისთვის გჭირდება)
requirements = python3,kivy==2.3.0,kivymd,pillow,openssl,requests,sh

# (list) ნებართვები (აქ არის ყველა საჭირო SMS და ინტერნეტ უფლება)
android.permissions = INTERNET, SEND_SMS, RECEIVE_SMS, READ_PHONE_STATE, READ_SMS, WAKE_LOCK

# (int) Android API პარამეტრები (API 33 აუცილებელია თანამედროვე ტელეფონებისთვის)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

# (list) არქიტექტურა (პირველ ბილდზე მხოლოდ ერთი დავტოვოთ სტაბილურობისთვის)
android.archs = arm64-v8a

# (bool) ეკრანის პარამეტრები
fullscreen = 1
orientation = portrait

# (bool) ლიცენზიის ავტომატური დადასტურება
android.accept_sdk_license = True

# (bool) AndroidX მხარდაჭერა (KivyMD-სთვის აუცილებელია)
android.enable_androidx = True

# (str) P4A ბრენჩი
p4a.branch = master

[buildozer]
# (int) ლოგის დონე (2 ნიშნავს, რომ ყველა დეტალს დაგვიწერს)
log_level = 2

# (int) გაფრთხილება root-ზე
warn_on_root = 1
