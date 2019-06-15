pyinstaller -F --noconsole ^
--add-binary api.pyd;. ^
--add-binary commands.pyd;. ^
--add-binary dialogs.pyd;. ^
--add-binary database.pyd;. ^
--add-binary drawer.pyd;. ^
--add-binary configs.pyd;. ^
--add-binary tree.pyd;. ^
--add-binary wxdb.pyd;. ^
--hidden-import wx ^
main.pyw
