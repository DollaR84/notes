pyinstaller -F --noconsole -n notes ^
--add-binary actions/actions.pyd;actions ^
--add-binary actions/base.pyd;actions ^
--add-binary actions/history.pyd;actions ^
--add-binary actions/main.pyd;actions ^
--add-binary actions/extend.pyd;actions ^
--add-binary actions/order.pyd;actions ^
--add-binary actions/sort.pyd;actions ^
--add-binary dialogs/dialogs.pyd;dialogs ^
--add-binary dialogs/options.pyd;dialogs ^
--add-binary accessible.pyd;. ^
--add-binary api.pyd;. ^
--add-binary commands.pyd;. ^
--add-binary configs.pyd;. ^
--add-binary converter.pyd;. ^
--add-binary copy.pyd;. ^
--add-binary database.pyd;. ^
--add-binary drawer.pyd;. ^
--add-binary menu.pyd;. ^
--add-binary tables.pyd;. ^
--add-binary tree.pyd;. ^
--add-binary updates.pyd;. ^
--add-binary version.pyd;. ^
--add-binary wxdb.pyd;. ^
--hidden-import wx ^
--hidden-import os ^
--hidden-import sys ^
--hidden-import abc ^
--hidden-import hashlib ^
--hidden-import pickle ^
--hidden-import sqlite3 ^
--hidden-import webbrowser ^
main.pyw
