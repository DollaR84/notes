'''
Setup script build exe windows application.

created on 05.04.2020

@author: Ruslan Dolovanyuk

Example running: python setup.py build

'''

from cx_Freeze import setup, Executable

import version

executables = [Executable('main.pyw',
                          targetName='notes.exe',
                          base='Win32GUI')]

excludes = ['logging', 'unittest', 'email', 'html', 'http', 'urllib', 'xml', 'xmlrpc',
            'bz2', 'select', 'pydoc', 'ctypes', 'tkinter', 'distutils', 'test',
           ]

includes = ['pickle', 'webbrowser', 'wx',
'sqlite3',
           ]

zip_include_packages = ['collections', 'encodings', 'importlib',
                        'pickle', 'webbrowser', 'wx',
                        'sqlite3',
                       ]

include_files = [('commands.pyd', 'lib/commands.pyd'),
                  ('configs.pyd', 'lib/configs.pyd'),
                  ('database.pyd', 'lib/database.pyd'),
                  ('dialogs.pyd', 'lib/dialogs.pyd'),
                  ('menu.pyd', 'lib/menu.pyd'),
                  ('options.pyd', 'lib/options.pyd'),
                  ('version.pyd', 'lib/version.pyd'),
                  ('wxdb.pyd', 'lib/wxdb.pyd'),
                  ('api.pyd', 'lib/api.pyd'),
                  ('tree.pyd', 'lib/tree.pyd'),
                  'languages.dat',
                 ]

options = {
    'build_exe': {
        'include_msvcr': True,
        'excludes': excludes,
        'includes': includes,
        'zip_include_packages': zip_include_packages,
        'build_exe': 'build_windows',
        'include_files': include_files,
    }
}

setup(name='notes',
      version=version.VERSION,
      description='Saver notes in database on tree view.',
      executables=executables,
      options=options)
