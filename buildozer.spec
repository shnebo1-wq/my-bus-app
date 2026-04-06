name: Build Android APK
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          sudo apt update
          sudo apt install -y git zip unzip autoconf libtool pkg-config zlib1g-dev \
          libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev \
          python3-dev libgles2-mesa-dev libsdl2-dev libsdl2-image-dev \
          libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev \
          libavformat-dev libavcodec-dev libsqlite3-dev
          
          # აქ ვასწორებთ კრიტიკულ ვერსიებს
          pip install --upgrade pip
          pip install Cython==0.29.33
          pip install buildozer

      - name: Build with Buildozer
        run: |
          # ეს ბრძანება ავტომატურად ადასტურებს SDK-ს ლიცენზიებს
          yes | buildozer -v android debug
        env:
          BUILDOZER_WARN_ON_ROOT: 1

      - name: Upload APK
        uses: actions/upload-artifact@v3
        with:
          name: my-bus-app-apk
          path: bin/*.apk
