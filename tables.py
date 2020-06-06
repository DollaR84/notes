"""
Description tables for databases.

Created on 20.04.2020

@author: Ruslan Dolovanyuk

"""


VERSION = 5


SETTINGS = {
    "settings": [
        ["id", "INTEGER", "PRIMARY KEY", "NOT NULL"],
        ["name", "TEXT", "NOT NULL"],
        ["value", "TEXT", "NOT NULL"]
    ],
    "window": [
        ['id', 'INTEGER', 'PRIMARY KEY', 'NOT NULL'],
        ['px', 'INTEGER', 'NOT NULL'],
        ['py', 'INTEGER', 'NOT NULL'],
        ['sx', 'INTEGER', 'NOT NULL'],
        ['sy', 'INTEGER', 'NOT NULL']
    ],
    "states": [
        ["id", "INTEGER", "PRIMARY KEY", "NOT NULL"],
        ["state", "TEXT", "NOT NULL"]
    ]
}

NOTES = {
    "notes": [
        ["id", "INTEGER", "PRIMARY KEY", "NOT NULL"],
        ["title", "TEXT", "NOT NULL"],
        ["data", "TEXT", "NOT NULL"],
        ["parent", "INTEGER", "NOT NULL"],
    ],
    "expands": [
        ["id", "INTEGER", "PRIMARY KEY", "NOT NULL"],
        ["expand", "INTEGER", "NOT NULL"]
    ]
}


def get_tables_names(tables):
    """Return list all tables names from dict."""
    return [table for table in list(tables.keys())]


def get_columns_names(table):
    """Return list all columns names for table."""
    return [column[0] for column in table]


def test():
    """print test string format from TABLES."""
    table = 'notes'
    script = 'CREATE TABLE {} ({}) WITHOUT ROWID'.format(table,
        ', '.join([' '.join(row) for row in NOTES[table]]))
    print(script)

    tables = get_tables_names(NOTES)
    print(tables)
    columns = get_columns_names(NOTES[tables[1]])
    print(columns)


if __name__ == '__main__':
    test()
