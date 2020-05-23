"""
Converter database from old versions to new.

Created on 19.04.2020

@author: Ruslan Dolovanyuk

"""

import os

from datetime import datetime

from database import Database

import tables


class DBConverter:
    """Converter database on new update versions."""

    def __init__(self, db_name):
        """initialization converter database."""
        self.__db_name = db_name
        self.__db = Database()

        self.__update_functions = [
                                   'update_db2',
                                   'update_db3',
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
                else:
                    pass
        else:
            pass
        return tables.VERSION

    def __fix_data(self, row):
        """Fix data items from rows database."""
        result = []
        for item in row:
            if isinstance(item, int):
                result.append(str(item))
            elif isinstance(item, str):
                result.append('"{}"'.format(item))
            else:
                result.append(item)
        return result

    def __save_old_db(self, db_name, version):
        """Saving old databases before updates."""
        date = datetime.strftime(datetime.now(), "%d.%m.%Y")
        os.rename(''.join([db_name, '.db']), ''.join([db_name, '.v{}.'.format(version), date, '.db']))

    def update_db2(self):
        """Update database tables from version database 1 to version 2."""
        self.__db.connect(self.__db_name + '.db')
        self.__get_old_data(self.__db.get_tables_names())
        self.__db.disconnect()
        self.__save_old_db(self.__db_name, 1)
        self.__db.connect(self.__db_name + '.db')
        counter = {}
        for table, rows in self.__old_data.items():
            script = 'CREATE TABLE {} ({}) WITHOUT ROWID'.format(table,
                ', '.join([' '.join(row) for row in tables.NOTES[table]]))
            self.__db.put(script)
            for row in rows:
                row = self.__fix_data(row)
                columns = tables.get_columns_names(tables.NOTES[table])
                if table == 'notes':
                    parent = row[-1]
                    if parent not in counter:
                        counter[parent] = 0
                    counter[parent] += 1
                    script = 'INSERT INTO {} ({}) VALUES ({}, {})'.format(table,
                        ', '.join(columns),
                        ', '.join(row),
                        counter[parent])
                else:
                    script = 'INSERT INTO {} ({}) VALUES ({})'.format(table,
                        ', '.join(columns),
                        ', '.join(row))
                self.__db.put(script)
        self.__db.commit()
        self.__db.disconnect()

    def update_db3(self):
        """Update database tables from version database 2 to version 3."""
        self.__db.connect(self.__db_name + '.db')
        self.__get_old_data(self.__db.get_tables_names())
        self.__db.disconnect()
        self.__save_old_db(self.__db_name, 2)
        self.__db.connect(self.__db_name + '.db')
        for table, rows in self.__old_data.items():
            script = 'CREATE TABLE {} ({}) WITHOUT ROWID'.format(table,
                ', '.join([' '.join(row) for row in tables.NOTES[table]]))
            self.__db.put(script)
            for row in rows:
                row = self.__fix_data(row)
                columns = tables.get_columns_names(tables.NOTES[table])
                if table == 'notes':
                    script = 'INSERT INTO {} ({}) VALUES ({}, 0)'.format(table,
                        ', '.join(columns),
                        ', '.join(row))
                else:
                    script = 'INSERT INTO {} ({}) VALUES ({})'.format(table,
                        ', '.join(columns),
                        ', '.join(row))
                self.__db.put(script)
        self.__db.commit()
        self.__db.disconnect()

    def check_rows(self, db, tables_dict, updates_dict):
        """Add rows in updates databases."""
        for table, update_dict in updates_dict.items():
            for version, rows in update_dict.items():
                if version <= tables.VERSION:
                    if db.get_last_id(table) < int(rows[-1].split(', ')[0]):
                        columns = tables.get_columns_names(tables_dict[table])
                        for row in rows:
                            script = 'INSERT INTO {} ({}) VALUES ({})'.format(table, ', '.join(columns), row)
                            db.put(script)
                        db.commit()

    def run(self, tables_dict):
        """Run convert data from old database to new."""
        try:
            self.__db.connect(self.__db_name + '.db')
            db_ver = self.checker(self.__db, tables_dict)
            self.__db.disconnect()
            for index in range(db_ver-1, tables.VERSION-1):
                getattr(self, self.__update_functions[index])()
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
