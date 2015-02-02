@echo off
C:\Python27\python.exe C:\pyinstaller-2.1\pyinstaller.py .toolkit.py --onefile
move dist\.toolkit.exe toolkit.exe
"C:\Program Files (x86)\7-Zip\7z.exe" a acer_iconia_toolkit_v0.9.0.zip bin\ external2internal\ system_image\ README.md .toolkit.py toolkit.sh toolkit.exe changelog.txt

REM mv ${PWD##*\}.zip ..\

RD /s/q build
RD /s/q dist
REM DEL logdict2.7.*
DEL .toolkit.spec
pause
