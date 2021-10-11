@echo off
setlocal
set dependencies=TurboGears2 kajiki SQLAlchemy WebHelpers2 Beaker
set currentPath=%~dp0
REM create virtualenv if not exist
if not exist "%currentPath%env" (
    call virtualenv env
)
REM DO NOT FORGET!!! activate virtualenv
call %currentPath%env/Scripts/activate.bat
call pip install %dependencies%
call pip check
endlocal
pause