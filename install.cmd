pyinstaller -F --noconsole ^
--add-binary dialogs/dialogs.py;dialogs ^
--add-binary dialogs/settings.py;dialogs ^
--add-binary api.pyd;. ^
--add-binary commands.py;. ^
--add-binary configs.py;. ^
--add-binary database.py;. ^
--add-binary drawer.py;. ^
--add-binary tree.pyd;. ^
--add-binary wxdb.py;. ^
--hidden-import wx ^
main.pyw
