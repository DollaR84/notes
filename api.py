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
        self.phrases = phrases
        self.db = Database()
        self.__checker(message)
        self.db.connect(self.db_name + '.db')

        if not self.db.if_exists('notes'):
            self.setup()

    def close(self):
        """Save finish program."""
        self.db.disconnect()

    def __checker(self, message):
        """Check and run if needed convert BD notes from old version to new."""
        conv = DBConverter(self.db_name)
        self.db.connect(self.db_name + '.db')
        db_ver = conv.checker(self.db)
        self.db.disconnect()
        if db_ver != tables.VERSION:
            message.information(self.phrases.titles.info, self.phrases.conv.info % (db_ver, tables.VERSION,))
            conv.run()
            message.information(self.phrases.titles.info, self.phrases.conv.success % (tables.VERSION,))

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
        script = 'SELECT id, order_sort FROM notes WHERE parent=?'
        rows = self.db.get(script, parent_id)
        return {row[0]: row[1] for row in rows}

    def get_note(self, index):
        """Return note data from database."""
        script = 'SELECT data FROM notes WHERE id=?'
        row = self.db.get(script, index)
        return row[0][0]

    def create(self, index, title, parent_id, order_id):
        """Create new row in database."""
        script = '''INSERT INTO notes (id, title, data, parent, order_sort)
                    VALUES (?, ?, "", ?, ?)'''
        self.db.put(script, index, title, parent_id, order_id)
        self.db.commit()

    def save_title(self, index, title):
        """Save title note in database."""
        script = 'UPDATE notes SET title=? WHERE id=?'
        self.db.put(script, title, index)
        self.db.commit()

    def save_data(self, index, data):
        """Save data note in database."""
        script = 'UPDATE notes SET data=? WHERE id=?'
        self.db.put(script, data, index)
        self.db.commit()

    def del_note(self, index):
        """Delete note in database."""
        script = 'SELECT id, parent, order_sort FROM notes'
        rows = self.db.get(script)
        script = 'SELECT parent, order_sort FROM notes WHERE id=?'
        parent_id, order_sort = self.db.get(script, index)[0]
        script = 'SELECT id FROM notes WHERE parent=?'
        parent_order_last = len(self.db.get(script, parent_id))
        script = 'DELETE FROM notes WHERE id=?'
        self.db.put(script, index)
        childs = [row[0] for row in rows if row[1] == index]
        for i, value in enumerate(childs):
            if value > index:
                childs[i] = value - 1
        for row in rows:
            index_id = row[0] if (row[0] < index) else row[0]-1
            parent = row[1] if (row[1] < index) else row[1]-1
            if row[1] == parent_id:
                order = row[2] if (row[2] < order_sort) else row[2]-1
                script = 'UPDATE notes SET id=?, parent=?, order_sort=? WHERE id=?'
                self.db.put(script, index_id, parent, order, row[0])
            else:
                script = 'UPDATE notes SET id=?, parent=? WHERE id=?'
                self.db.put(script, index_id, parent, row[0])
        for child in childs:
            script = 'UPDATE notes SET parent=?, order_sort=? WHERE id=?'
            self.db.put(script, parent_id, parent_order_last, child)
            parent_order_last += 1
        self.db.commit()
        script = 'DELETE FROM expands WHERE id=?'
        self.db.put(script, index)
        self.db.commit()

    def update(self, items):
        """Update order_sort param notes in database.

        Input parameters:
        items: dict {id: (parent, order_sort)};

        """
        for index, value in items.items():
            script = 'UPDATE notes SET parent=?, order_sort=? WHERE id=?'
            self.db.put(script, value[0], value[1], index)
            self.db.commit()

    def get_expands(self):
        """Return dict all expand rows."""
        script = 'SELECT * FROM expands'
        rows = self.db.get(script)
        return {row[0]: row[1] for row in rows}

    def set_expands(self, expands):
        """Set expand value saving in database."""
        script = 'DELETE FROM expands'
        self.db.put(script)
        for index, expand in expands.items():
            script = '''INSERT INTO expands (id, expand)
                        VALUES (?, ?)'''
            self.db.put(script, index, expand)
        self.db.commit()

    def setup(self):
        """Create tables in database."""
        for table in ['notes', 'expands']:
            script = 'CREATE TABLE {} ({}) WITHOUT ROWID'.format(table,
                ', '.join([' '.join(row) for row in tables.TABLES[table]]))
            self.db.put(script)
        self.db.commit()
