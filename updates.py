"""
Updates module.

Created on 22.05.2020

@author: Ruslan Dolovanyuk

"""

from collections import OrderedDict

from copy import deepcopy


COLUMNS = {
    "notes": OrderedDict([
        (2, [
            ["order_sort", "INTEGER", "NOT NULL"],
        ]),
        (3, [
            ["readonly", "INTEGER", "NOT NULL"],
        ]),
    ])
}


ROWS = {
    "settings": OrderedDict([
        (3, [
            '4, "readonly_password_check", "false"',
            '5, "readonly_password", ""'
        ])
    ])
}


def update(tables, data):
    """Update tables and add rows in data."""
    tables_dict = deepcopy(tables)
    default_data = deepcopy(data)
    for table, rows in default_data.items():
        update_dict = COLUMNS.get(table, {})
        tables_dict[table].extend([line for lst in update_dict.values() for line in lst])
        update_dict = ROWS.get(table, {})
        rows.extend([line for lst in update_dict.values() for line in lst])
    return tables_dict, default_data


def columns_all(table, version):
    """Return updates all columns for version table."""
    result = []
    for ver, upd in COLUMNS.get(table, {}).items():
        if ver <= version:
            result.extend(upd)
    return result


def columns(table, version):
    """Return updates columns for version table."""
    return COLUMNS.get(table, {}).get(version, [])


def rows(table, version):
    """Return updates rows for version table."""
    return ROWS.get(table, {}).get(version, [])
