[app]
title = RSS Control Pro
package.name = rss_commander
package.domain = org.rss.bus
source.dir = .
# დავამატე charset-normalizer და idna - ესენი requests-ს სჭირდება
source.include_exts = py,png,jpg,kv,ttf,json,dat
version = 1.0.0

icon.filename = logo.png
presplash.filename = logo.png

# კრიტიკული ცვლილება: დავამატე charset-normalizer, idna და კოდში გამოყენებული jnius (pyjnius)
requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests,urllib3,certifi,charset-normalizer,idna,pyjnius

orientation = portrait

# დავამატე შიდა მეხსიერებაზე წვდომა ბაზის შესანახად
android.permissions = INTERNET, SEND_SMS, RECEIVE_SMS, READ_PHONE_STATE, WAKE_LOCK, READ_SMS, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.jdk = 17

# ეს აუცილებელია, რომ აპლიკაციამ თავის პრივატულ საქაღალდეში შეინახოს .dat და .json ფაილები
android.private_storage = True
android.accept_sdk_license = True

# თუ მხოლოდ შენს ტელეფონზე ტესტავ, arm64-v8a კარგია. 
# თუ გინდა სხვადასხვა ანდროიდებზე წავიდეს, დაამატე: armeabi-v7a
android.archs = arm64-v8a

android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
