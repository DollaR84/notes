"""
API for work with notes.

Created on 31.05.2019

@author: Ruslan Dolovanyuk

"""

from database import Database


class Notes:
    """Api class for work notes."""

    def __init__(self, config):
        """Initialize notes class."""
        self.config = config

        self.db = Database()
        self.db.connect(self.config.name + '.db')

        if not self.db.if_exists(self.config.name):
            self.setup()

    def close(self):
        """Finish programm work."""
        self.db.disconnect()

    def setup(self):
        """Create table notes in database."""
        scripts = []
        script = '''CREATE TABLE %s (
                    id INTEGER PRIMARY KEY NOT NULL,
                    name TEXT NOT NULL,
                    value TEXT NOT NULL) WITHOUT ROWID
                 ''' % self.config.name
        scripts.append(script)
        script = '''INSERT INTO settings (id, name, value)
                    VALUES (1, "name", "notes")'''
        scripts.append(script)
        self.db.put(scripts)

