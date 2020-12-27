#!/bin/sh

cleanup () {
    echo "~~ CLEAN UP ~~"
}
trap cleanup EXIT

EXEC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
USAGE=""
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -s|--device) DEVICE="$2"; shift ;;
        -u|--uglify) uglify=1 ;;
        -h|--help) echo $USAGE; exit 0;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

if [ -z "$DEVICE" ]; then
  DEVICE=${adb devices | sed -n 2p | awk '{print $1;}'}
fi

if [ -z "$DEVICE" ]; then
  echo "No devices or emulators attached"
fi
