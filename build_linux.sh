#!/bin/bash
wine ~/.wine/dosdevices/c\:/Python27/python.exe ~/.wine/dosdevices/c\:/pyinstaller-2.0/pyinstaller.py .toolkit.py --onefile
mv dist/.toolkit.exe toolkit.exe

7z a ${PWD##*/}.zip bin/ external2internal/ system_image/ README.md .toolkit.py toolkit.sh toolkit.exe changelog.txt
mv ${PWD##*/}.zip ../

rm -rf build
rm -rf dist
rm logdict2.7.*
rm .toolkit.spec
