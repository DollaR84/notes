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
        return (row[0][0], row[0][1])

    def create(self, index, parent_id):
        """Create new row in database."""
        script = '''INSERT INTO notes (id, title, data, parent)
                    VALUES (%d, "Новая заметка", "", %d)''' % (index, parent_id)
        self.db.put(script)

    def save(self, index, title, data):
        """Save note in database."""
        script = 'UPDATE notes SET title="%s", data="%s" WHERE id=%d' % (title, data, index)
        self.db.put(script)

    def get_expands(self):
        """Return dict all expand rows."""
        script = 'SELECT * FROM expands'
        rows = self.db.get(script)
        return {row[0]: row[1] for row in rows}

    def set_expands(self, expands):
        """Set expand value saving in database."""
        scripts = []
        script = 'DELETE FROM expands'
        scripts.append(script)
        for index, expand in expands.items():
            script = '''INSERT INTO expands (id, expand)
                        VALUES (%d, %d)''' % (index, expand)
            scripts.append(script)
        self.db.put(scripts)

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
        script = '''CREATE TABLE expands (
                    id INTEGER PRIMARY KEY NOT NULL,
                    expand INTEGER NOT NULL) WITHOUT ROWID
                 '''
        scripts.append(script)
        self.db.put(scripts)
