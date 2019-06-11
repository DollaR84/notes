"""
Configs module.

Created on 25.05.2019

@author: Ruslan Dolovanyuk

"""

from dialogs.dialogs import RetCode

from dialogs.settings import SettingsDialog

from wxdb import WXDB


class Config(WXDB):
    """Config program in database."""

    def __init__(self):
        """Initialization config class."""
        super().__init__('notes')

        if not self.db.if_exists('settings'):
            self.setup_config()

        self.load()

    def load(self):
        """Load settings from database."""
        script = 'SELECT * FROM settings'
        data = self.db.get(script)
        self.ids = {}
        for line in data:
            setattr(self, line[1], line[2])
            self.ids[line[1]] = line[0]

    def open_settings(self, parent):
        """Open settings dialog."""
        dlg = SettingsDialog(parent, self)
        if RetCode.OK == dlg.ShowModal():
            dlg.get_all()
            scripts = []
            for key, value in dlg.config.items():
                script = '''UPDATE settings SET value="%s" WHERE id=%d
                     ''' % (value, self.ids[key])
                scripts.append(script)
            self.db.put(scripts)
        dlg.Destroy()
        self.load()

    def setup_config(self):
        """Create table settings in database."""
        scripts = []
        script = '''CREATE TABLE settings (
                    id INTEGER PRIMARY KEY NOT NULL,
                    name TEXT NOT NULL,
                    value TEXT NOT NULL) WITHOUT ROWID
                 '''
        scripts.append(script)
        script = '''INSERT INTO settings (id, name, value)
                    VALUES (1, "root", "Заметки")'''
        scripts.append(script)
        script = '''INSERT INTO settings (id, name, value)
                    VALUES (2, "general_expand", "true")'''
        scripts.append(script)
        self.db.put(scripts)
