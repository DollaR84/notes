pyinstaller -F --noconsole ^
--add-binary dialogs/dialogs.pyd;dialogs ^
--add-binary dialogs/options.pyd;dialogs ^
--add-binary api.pyd;. ^
--add-binary commands.pyd;. ^
--add-binary configs.pyd;. ^
--add-binary database.pyd;. ^
--add-binary drawer.pyd;. ^
--add-binary menu.pyd;. ^
--add-binary tree.pyd;. ^
--add-binary version.pyd;. ^
--add-binary wxdb.pyd;. ^
--hidden-import wx ^
--hidden-import pickle ^
--hidden-import sqlite3 ^
--hidden-import webbrowser ^
main.pyw
