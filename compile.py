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
               Extension("api", ["api.py"]),
               Extension("commands", ["commands.py"]),
               Extension("dialogs", ["dialogs/dialogs.py"]),
               Extension("dialogs", ["dialogs/settings.py"]),
               Extension("drawer", ["drawer.py"]),
               Extension("configs", ["configs.py"]),
               Extension("database", ["database.py"]),
               Extension("tree", ["tree.py"]),
               Extension("wxdb", ["wxdb.py"])
              ]

setup(
      name='main',
      cmdclass={'build_ext': build_ext},
      ext_modules=ext_modules
)