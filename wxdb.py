"""
Module settings wx with database.

Created on 25.05.2019

@author: Ruslan Dolovanyuk

"""

import sys

from converter import DBConverter

from database import Database

import tables

import updates


class WXDB:
    """Class default settings gui wx in database."""

    def __init__(self, db_name):
        """Initialization base class settings wx in database."""
        self.db_name = db_name
        self.db = Database()

        self.db.connect(self.db_name + '.db')
        if not self.db.if_exists('window'):
            self.setup_wxdb()

    def close(self):
        """Save finish program."""
        self.db.disconnect()

    def checker(self, message, phrases):
        """Check and run if needed convert BD settings from old version to new."""
        conv = DBConverter(self.db_name)
        db_ver = conv.checker(self.db, tables.SETTINGS)
        if db_ver != tables.VERSION:
            self.db.disconnect()
            message.information(phrases.titles.info, phrases.conv.info % (db_ver, tables.VERSION,))
            if conv.run(tables.SETTINGS):
                message.information(phrases.titles.info, phrases.conv.success % (tables.VERSION,))
            else:
                message.information(phrases.titles.error, phrases.conv.error)
                sys.exit()
            self.db.connect(self.db_name + '.db')
        conv.check_rows(self.db, tables.SETTINGS, updates.SETTINGS)

    def get_pos(self):
        """Return position window."""
        script = 'SELECT px, py FROM window'
        return self.db.get(script)[0]

    def set_pos(self, pos):
        """Save position window."""
        script = 'UPDATE window SET px=?, py=? WHERE id=1'
        self.db.put(script, *pos)
        self.db.commit()

    def get_size(self):
        """Return size window."""
        script = 'SELECT sx, sy FROM window'
        return self.db.get(script)[0]

    def set_size(self, size):
        """Save size window."""
        script = 'UPDATE window SET sx=?, sy=? WHERE id=1'
        self.db.put(script, *size)
        self.db.commit()

    def setup_wxdb(self):
        """Create tables this module."""
        self.db.setup(tables.SETTINGS, tables.get_columns_names, DEFAULT_DATA)


DEFAULT_DATA = {
    "window": [
        '1, 0, 0, 480, 320',
    ],
}
