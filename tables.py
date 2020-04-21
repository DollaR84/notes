"""
Description tables for databases.

Created on 20.04.2020

@author: Ruslan Dolovanyuk

"""


VERSION = 2


TABLES = {
    "settings": [
        ["id", "INTEGER", "PRIMARY KEY", "NOT NULL"],
        ["name", "TEXT", "NOT NULL"],
        ["value", "TEXT", "NOT NULL"]
    ],
    "notes": [
        ["id", "INTEGER", "PRIMARY KEY", "NOT NULL"],
        ["title", "TEXT", "NOT NULL"],
        ["data", "TEXT", "NOT NULL"],
        ["parent", "INTEGER", "NOT NULL"],
        ["order_sort", "INTEGER", "NOT NULL"]
    ],
    "expands": [
        ["id", "INTEGER", "PRIMARY KEY", "NOT NULL"],
        ["expand", "INTEGER", "NOT NULL"]
    ]
}


def get_tables_names():
    """Return list all tables names."""
    return [table for table in list(TABLES.keys())]


def get_columns_names(table):
    """Return list all columns names for table."""
    return [column[0] for column in TABLES[table]]


def test():
    """print test string format from TABLES."""
    table = 'notes'
    script = 'CREATE TABLE {} ({}) WITHOUT ROWID'.format(table,
        ', '.join([' '.join(row) for row in TABLES[table]]))
    print(script)

    tables = get_tables_names()
    print(tables)
    columns = get_columns_names(tables[1])
    print(columns)


if __name__ == '__main__':
    test()
