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

# (str) Application versioning
version = 1.0.0

# --- ლოგო და ჩატვირთვის ეკრანი ---
# დარწმუნდი, რომ logo.png გიდევს იმავე პაპკაში, სადაც main.py
icon.filename = logo.png
presplash.filename = logo.png

# (list) Application requirements
requirements = python3,kivy,kivymd,requests,urllib3,certifi

# (str) Supported orientation
# დატოვე portrait ბილდის წარმატებით დასრულებისთვის
orientation = portrait

# (list) Permissions (SMS-ისთვის აუცილებელი ნებართვები)
android.permissions = INTERNET, SEND_SMS, RECEIVE_SMS, READ_PHONE_STATE, WAKE_LOCK, READ_SMS

# (int) Target Android API
android.api = 33

# (int) Minimum API support
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (str) Android JDK version
android.jdk = 17

# (bool) Use --private data storage
android.private_storage = True

# (bool) Accept SDK license
android.accept_sdk_license = True

# (str) The Android arch to build for (GitHub-ზე ერთი ჯობია)
android.archs = arm64-v8a

# (bool) Enable Androidx
android.enable_androidx = True

# (bool) Skip byte compile to save space/time
android.no_byte_compile_python_optimization = 1

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1

# (str) Path to build artifacts
bin_dir = ./bin
