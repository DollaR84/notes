"""
Converter database from old versions to new.

Created on 19.04.2020

@author: Ruslan Dolovanyuk

"""

from copy import deepcopy
from datetime import datetime
import os

from database import Database

import tables

import updates


class DBConverter:
    """Converter database on new update versions."""

    def __init__(self, db_name):
        """initialization converter database."""
        self.__db_name = db_name
        self.__db = Database()

        self.__update_functions = [
                                   'update_db2',
                                   'update_db3',
                                   'update_db4',
                                   'update_db5',
                                  ]

    def __get_old_data(self, tables_list):
        """Get all data from old database."""
        self.__old_data = {table: self.__db.get("SELECT * FROM %s" % table) for table in tables_list}

    def checker(self, db, tables_dict):
        """Check and return version input database."""
        tables_db = db.get_tables_names()
        tables_cr = tables.get_tables_names(tables_dict)
        diff_tables = list(set(tables_cr) - set(tables_db))
        if not diff_tables:
            for table in tables_cr:
                columns_db = db.get_columns_names(table)
                diff_columns = list(set(tables.get_columns_names(tables_dict[table])) - set(columns_db))
                if 'order_sort' in diff_columns:
                    return 1
                elif 'readonly' in diff_columns:
                    return 2
                elif ('date_create' in diff_columns) and ('date_update' in diff_columns):
                    return 3
                elif ('state_check' in diff_columns) and ('state' in diff_columns):
                    return 4
                else:
                    pass
        elif 'states' in diff_tables:
            return 4
        else:
            pass
        return tables.VERSION

    def __save_old_db(self, db_name, version):
        """Saving old databases before updates."""
        date = datetime.strftime(datetime.now(), "%d.%m.%Y")
        time = datetime.strftime(datetime.now(), "%H.%M.%S")
        try:
            os.rename(''.join([db_name, '.db']), ''.join([db_name, '.v{}.'.format(version), date, '.db']))
        except:
            os.rename(''.join([db_name, '.db']), ''.join([db_name, '.v{}.'.format(version), date, '.', time, '.db']))

    def update_db(self, db_ver, tables_dict_default, update_func):
        """Run update database tables."""
        self.__db.connect(self.__db_name + '.db')
        self.__get_old_data(self.__db.get_tables_names())
        self.__db.disconnect()
        self.__save_old_db(self.__db_name, db_ver)
        self.__db.connect(self.__db_name + '.db')
        tables_dict = deepcopy(tables_dict_default)
        for table in tables_dict.keys():
            tables_dict[table].extend(updates.columns_all(table, db_ver+1))
            script = 'CREATE TABLE {} ({}) WITHOUT ROWID'.format(table,
                ', '.join([' '.join(row) for row in tables_dict[table]]))
            self.__db.put(script)
            columns = tables.get_columns_names(tables_dict[table])
            rows = self.__old_data.get(table, [])
            update_func(table, columns, rows)
        self.__db.commit()
        self.__db.disconnect()

    def update_db2(self, table, columns, rows):
        """Update database tables from version database 1 to version 2."""
        counter = {}
        for row in rows:
            if table == 'notes':
                parent = row[-1]
                if parent not in counter:
                    counter[parent] = 0
                counter[parent] += 1
                script = 'INSERT INTO {} ({}) VALUES ({}, {})'.format(table,
                    ', '.join(columns),
                    ', '.join(['?' for _ in range(len(row))]),
                    counter[parent])
            else:
                script = 'INSERT INTO {} ({}) VALUES ({})'.format(table,
                    ', '.join(columns),
                    ', '.join(['?' for _ in range(len(row))]))
            self.__db.put(script, *row)

    def update_db3(self, table, columns, rows):
        """Update database tables from version database 2 to version 3."""
        for row in rows:
            if table == 'notes':
                script = 'INSERT INTO {} ({}) VALUES ({}, 0)'.format(table,
                    ', '.join(columns),
                    ', '.join(['?' for _ in range(len(row))]))
            else:
                script = 'INSERT INTO {} ({}) VALUES ({})'.format(table,
                    ', '.join(columns),
                    ', '.join(['?' for _ in range(len(row))]))
            self.__db.put(script, *row)

    def update_db4(self, table, columns, rows):
        """Update database tables from version database 3 to version 4."""
        for row in rows:
            if table == 'notes':
                script = 'INSERT INTO {} ({}) VALUES ({}, "", "")'.format(table,
                    ', '.join(columns),
                    ', '.join(['?' for _ in range(len(row))]))
            else:
                script = 'INSERT INTO {} ({}) VALUES ({})'.format(table,
                    ', '.join(columns),
                    ', '.join(['?' for _ in range(len(row))]))
            self.__db.put(script, *row)

    def update_db5(self, table, columns, rows):
        """Update database tables from version database 4 to version 5."""
        for row in rows:
            if table == 'notes':
                script = 'INSERT INTO {} ({}) VALUES ({}, 0, "")'.format(table,
                    ', '.join(columns),
                    ', '.join(['?' for _ in range(len(row))]))
            else:
                script = 'INSERT INTO {} ({}) VALUES ({})'.format(table,
                    ', '.join(columns),
                    ', '.join(['?' for _ in range(len(row))]))
            self.__db.put(script, *row)

    def check_rows(self, db, tables_dict):
        """Add rows in updates databases."""
        for table in list(tables_dict.keys()):
            update_dict = updates.ROWS.get(table, {})
            for version, rows in update_dict.items():
                if version <= tables.VERSION:
                    if db.get_last_id(table) < int(rows[-1].split(', ')[0]):
                        columns = tables.get_columns_names(tables_dict[table])
                        for row in rows:
                            script = 'INSERT INTO {} ({}) VALUES ({})'.format(table, ', '.join(columns), row)
                            db.put(script)
                        db.commit()

    def run(self, tables_dict_default, tables_dict):
        """Run convert data from old database to new."""
        try:
            self.__db.connect(self.__db_name + '.db')
            db_ver = self.checker(self.__db, tables_dict)
            self.__db.disconnect()
            for index in range(db_ver-1, tables.VERSION-1):
                self.update_db(index+1, tables_dict_default, getattr(self, self.__update_functions[index]))
        except Exception as e:
            print(e)
            return False
        return True


def main():
    """Main running this script."""
    dbconv = DBConverter('notes')
    dbconv.run()


if __name__ == "__main__":
    main()
