@echo off
setlocal
set pythonpath=%~dp0
call %pythonpath%env/Scripts/python.exe com/keksovmen/main.py
endlocal