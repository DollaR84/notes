"""
Compile module in python library pid.

Created on 15.06.2019

@author: Ruslan Dolovanyuk

example running:
    python compile.py build_ext --inplace

"""

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
               Extension("dialogs.dialogs", ["dialogs/dialogs.py"]),
               Extension("dialogs.options", ["dialogs/options.py"]),
               Extension("actions.actions", ["actions/actions.py"]),
               Extension("actions.base", ["actions/base.py"]),
               Extension("actions.history", ["actions/history.py"]),
               Extension("actions.main", ["actions/main.py"]),
               Extension("actions.order", ["actions/order.py"]),
               Extension("actions.sort", ["actions/sort.py"]),
               Extension("api", ["api.py"]),
               Extension("copy", ["copy.py"]),
               Extension("commands", ["commands.py"]),
               Extension("drawer", ["drawer.py"]),
               Extension("menu", ["menu.py"]),
               Extension("configs", ["configs.py"]),
               Extension("converter", ["converter.py"]),
               Extension("database", ["database.py"]),
               Extension("tables", ["tables.py"]),
               Extension("tree", ["tree.py"]),
               Extension("updates", ["updates.py"]),
               Extension("version", ["version.py"]),
               Extension("wxdb", ["wxdb.py"])
              ]

for e in ext_modules:
    e.cython_directives = {'language_level': "3"} #all are Python-3

setup(
      name='main',
      cmdclass={'build_ext': build_ext},
      ext_modules=ext_modules
)
