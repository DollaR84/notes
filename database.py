"""
This module work with databases on sqlite.

Created on 17.02.2018

@author: Ruslan Dolovanyuk

"""

import sqlite3


class Database:
    """The class for work databases on sqlite."""

    def __init__(self):
        """Initialize class for control databases."""
        self.conn = None
        self.cursor = None

    def connect(self, file_name):
        """Connect database."""
        self.conn = sqlite3.connect(file_name)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        """Disconnect database."""
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()

    def get(self, script, *args):
        """Get data from database."""
        self.cursor.execute(script, args)
        return self.cursor.fetchall()

    def put(self, script, *args):
        """Set data in database."""
        self.cursor.execute(script, args)

    def commit(self):
        """Commit all putting rows in database."""
        self.conn.commit()

    def if_exists(self, table):
        """Check table if exist in database."""
        str_sql = 'SELECT * FROM sqlite_master WHERE name = "%s"' % table
        self.cursor.execute(str_sql)
        if self.cursor.fetchone():
            return True
        return False

    def get_tables_names(self):
        """Return list tables names from database."""
        str_sql = 'SELECT name FROM sqlite_master WHERE type = "table"'
        self.cursor.execute(str_sql)
        return [table[0] for table in self.cursor.fetchall()]

    def get_params(self, table):
        """Return list params table from database."""
        str_sql = 'PRAGMA TABLE_INFO(%s)' % table
        self.cursor.execute(str_sql)
        return self.cursor.fetchall()

    def get_columns_names(self, table):
        """Return list names columns table from database."""
        params = self.get_params(table)
        return [param[1] for param in params]

    def get_last_id(self, table):
        """Return last id from table."""
        self.cursor.execute('SELECT id FROM {} ORDER BY id DESC LIMIT 1'.format(table))
        row = self.cursor.fetchone()
        return row[0]

    def dump(self, filename):
        """Dump database in sql file."""
        with open(filename, 'w', encoding='utf-8') as sql:
            self.dumpf(sql)

    def dumpf(self, file_sql):
        """Dump database in sql file."""
        for line in self.conn.iterdump():
            file_sql.write('%s\n' % line)

    def restore(self, filename):
        """Restore database from sql file."""
        with open(filename, 'r', encoding='utf-8') as sql:
            self.restoref(sql)

    def restoref(self, file_sql):
        """Restore database from sql file."""
        self.cursor.executescript(file_sql.read())
        self.commit()

    def setup(self, tables, get_columns_names_func, default_data):
        """Create table in database."""
        for table, params in default_data.items():
            script = 'CREATE TABLE {} ({}) WITHOUT ROWID'.format(table,
                ', '.join([' '.join(row) for row in tables[table]]))
            self.put(script)
            for substr in params:
                script = 'INSERT INTO {} ({}) VALUES ({})'.format(table,
                    ', '.join(get_columns_names_func(tables[table])),
                    substr)
                self.put(script)
        self.commit()
