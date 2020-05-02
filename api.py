"""
API for work with notes.

Created on 31.05.2019

@author: Ruslan Dolovanyuk

"""

from converter import DBConverter

from database import Database

import tables


class Notes:
    """Api class for work notes."""

    def __init__(self, message, phrases):
        """Initialize notes class."""
        self.db_name = 'notes'
        self.db = Database()
        self.__checker(message, phrases)
        self.db.connect(self.db_name + '.db')

        if not self.db.if_exists('notes'):
            self.setup()

    def close(self):
        """Save finish program."""
        self.db.disconnect()

    def __checker(self, message, phrases):
        """Check and run if needed convert BD notes from old version to new."""
        conv = DBConverter(self.db_name)
        self.db.connect(self.db_name + '.db')
        db_ver = conv.checker(self.db)
        self.db.disconnect()
        if db_ver != tables.VERSION:
            message.information(phrases.titles.info, phrases.conv.info % (db_ver, tables.VERSION,))
            conv.run()
            message.information(phrases.titles.info, phrases.conv.success % (tables.VERSION,))

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

    def get_order(self, parent_id):
        """Return dict orders childs from database by parent."""
        script = 'SELECT id, order_sort FROM notes WHERE parent=%d' % parent_id
        rows = self.db.get(script)
        return {row[0]: row[1] for row in rows}

    def get_note(self, index):
        """Return note title and data from database."""
        script = 'SELECT title, data FROM notes WHERE id=%d' % index
        row = self.db.get(script)
        return (row[0][0], row[0][1])

    def create(self, index, parent_id, order_id):
        """Create new row in database."""
        script = '''INSERT INTO notes (id, title, data, parent, order_sort)
                    VALUES (%d, "Новая заметка", "", %d, %d)''' % (index, parent_id, order_id)
        self.db.put(script)

    def save(self, index, title, data):
        """Save note in database."""
        script = 'UPDATE notes SET title="%s", data="%s" WHERE id=%d' % (title, data, index)
        self.db.put(script)

    def del_note(self, index):
        """Delete note in database."""
        script = 'SELECT id, parent, order_sort FROM notes'
        rows = self.db.get(script)
        script = 'SELECT parent, order_sort FROM notes WHERE id=%d' % index
        parent_id, order_sort = self.db.get(script)[0]
        script = 'SELECT id FROM notes WHERE parent=%d' % parent_id
        parent_order_last = len(self.db.get(script))
        scripts = []
        script = 'DELETE FROM notes WHERE id=%d' % index
        scripts.append(script)
        childs = [row[0] for row in rows if row[1] == index]
        for i, value in enumerate(childs):
            if value > index:
                childs[i] = value - 1
        for row in rows:
            index_id = row[0] if (row[0] < index) else row[0]-1
            parent = row[1] if (row[1] < index) else row[1]-1
            if row[1] == parent_id:
                order = row[2] if (row[2] < order_sort) else row[2]-1
                script = 'UPDATE notes SET id=%d, parent=%d, order_sort=%d WHERE id=%d' % (index_id, parent, order, row[0])
            else:
                script = 'UPDATE notes SET id=%d, parent=%d WHERE id=%d' % (index_id, parent, row[0])
            scripts.append(script)
        self.db.put(scripts)
        scripts.clear()
        for child in childs:
            script = 'UPDATE notes SET parent=%d, order_sort=%d WHERE id=%d' % (parent_id, parent_order_last, child)
            scripts.append(script)
            parent_order_last += 1
        self.db.put(scripts)
        script = 'DELETE FROM expands WHERE id=%d' % index
        self.db.put(script)

    def update(self, items):
        """Update order_sort param notes in database.

        Input parameters:
        items: dict {id: (parent, order_sort)};

        """
        scripts = []
        for index, value in items.items():
            script = 'UPDATE notes SET parent=%d, order_sort=%d WHERE id=%d' % (value[0], value[1], index)
            scripts.append(script)
        self.db.put(scripts)

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
        """Create tables in database."""
        scripts = []
        for table in ['notes', 'expands']:
            script = 'CREATE TABLE {} ({}) WITHOUT ROWID'.format(table,
                ', '.join([' '.join(row) for row in tables.TABLES[table]]))
            scripts.append(script)
        self.db.put(scripts)
