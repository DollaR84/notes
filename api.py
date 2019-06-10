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

    def get_titles(self):
        """Return dict titles from database."""
        script = 'SELECT id, title FROM notes'
        rows = self.db.get(script)
        return {row[0]: row[1] for row in rows}

    def get_parents(self):
        """Return dict parents from database."""
        script = 'SELECT id, parent FROM notes'
        rows = self.db.get(script)
        return {row[0]: row[1] for row in rows}

    def get_note(self, index):
        """Return note title and data from database."""
        script = 'SELECT title, data FROM notes WHERE id=%d' % index
        row = self.db.get(script)
        return (row[0], row[1])

    def setup(self):
        """Create table notes in database."""
        scripts = []
        script = '''CREATE TABLE notes (
                    id INTEGER PRIMARY KEY NOT NULL,
                    title TEXT NOT NULL,
                    data TEXT NOT NULL,
                    parent INTEGER NOT NULL) WITHOUT ROWID
                 '''
        scripts.append(script)
        self.db.put(scripts)
