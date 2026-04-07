name: Build APK
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Install Dependencies
        run: |
          sudo apt update
          sudo apt install -y git zip unzip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev python3-dev
          pip3 install --user --upgrade Cython==0.29.33 virtualenv buildozer
          # PATH-ის დამატება რომ სისტემამ buildozer დაინახოს
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      - name: Build with Buildozer
        run: |
          # 'yes' აუცილებელია ლიცენზიებზე დასათანხმებლად
          yes | buildozer -v android debug

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: package
          path: bin/*.apk
