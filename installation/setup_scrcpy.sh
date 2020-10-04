#!/bin/sh

finish() {
  # Your cleanup code here
  echo "~~Returning to directory~~"
  cd $DIR
}
trap finish EXIT

DIR=$(pwd)
SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "~~Going to [$SCRIPTDIR]~~"
cd $SCRIPTDIR

echo "~~Downloading SCRCPY-SERVER 1.16~~"
SERVERDIR="server"
mkdir $SERVERDIR
cd $SERVERDIR 
wget https://github.com/Genymobile/scrcpy/releases/download/v1.16/scrcpy-server-v1.16
mv scrcpy-server-v1.16 scrcpy-server
echo "    ~~Download complete~~"
cd ..

echo "~~Installing dependencies~~"
# runtime dependencies
sudo apt install ffmpeg libsdl2-2.0-0 adb --yes

# client build dependencies
sudo apt install gcc git pkg-config meson ninja-build \
                 libavcodec-dev libavformat-dev libavutil-dev \
                 libsdl2-dev --yes

# server build dependencies
sudo apt install openjdk-8-jdk --yes

echo "~~Manual build of SCRCPY~~"
echo "    ~~Cloning repository~~"
git clone https://github.com/Genymobile/scrcpy
cd scrcpy

echo "    ~~Starting build~~ [$(pwd)]"
meson x --buildtype release --strip -Db_lto=true \
    -Dprebuilt_server=$SCRIPTDIR/$SERVERDIR/scrcpy-server
ninja -Cx
sudo ninja -Cx install

echo "    ~~DONE~~"
