@echo off
set pyinstallerPath=E:\Programm\Python\Scripts\pyinstaller
set mainRelativePath=com/keksovmen/main.py
set exeName=CardNotebook
set arguments= -y ^
--name %exeName% ^
--paths env/Lib/site-packages ^
--add-data com/keksovmen/Controllers/xhtml;com/keksovmen/Controllers/xhtml ^
--add-data public;public ^
--icon public/icon.ico
call %pyinstallerPath% %mainRelativePath% %arguments%
