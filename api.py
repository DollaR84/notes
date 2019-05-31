"""
API for work with notes.

Created on 31.05.2019

@author: Ruslan Dolovanyuk

"""


class Notes:
    """Api class for work notes."""

    def __init__(self, config):
        """Initialize notes class."""
        self.config = config
        self.db = self.config.db

        if not self.db.if_exists('notes'):
            self.setup()

    def setup(self):
        """Create table notes in database."""
        scripts = []
        script = '''CREATE TABLE notes (
                    id INTEGER PRIMARY KEY NOT NULL,
                    name TEXT NOT NULL,
                    value TEXT NOT NULL) WITHOUT ROWID
                 '''
        scripts.append(script)
        self.db.put(scripts)
