"""
Configs module.

Created on 25.05.2019

@author: Ruslan Dolovanyuk

"""

import pickle

from dialogs.dialogs import RetCode

from dialogs.options import SettingsDialog

import tables

import updates

from wxdb import WXDB


class Config(WXDB):
    """Config program in database."""

    def __init__(self):
        """Initialization config class."""
        super().__init__('settings')

        if not self.db.if_exists('settings'):
            self.setup_config()

        self.load()
        self.set_languages()

    def load(self):
        """Load settings from database."""
        script = 'SELECT * FROM settings'
        data = self.db.get(script)
        self.ids = {}
        for line in data:
            setattr(self, line[1], line[2])
            self.ids[line[1]] = line[0]

    def set_languages(self):
        """Set all supported languages from languages pack."""
        with open('languages.dat', 'rb') as lang_file:
            self.__languages = pickle.load(lang_file)['languages']

    def get_languages(self):
        """Return dict all supported languages."""
        return self.__languages

    def get_language(self, code):
        """Return dict language from code."""
        with open('languages.dat', 'rb') as lang_file:
            return pickle.load(lang_file)[code]

    def open_settings(self, parent):
        """Open settings dialog."""
        result = False
        dlg = SettingsDialog(parent, self)
        if RetCode.OK == dlg.ShowModal():
            dlg.config.pop('donate_url')
            dlg.config.pop('languages')
            for key, value in dlg.config.items():
                if key == '__languages':
                    continue
                script = '''UPDATE settings SET value=? WHERE id=?'''
                self.db.put(script, value, self.ids[key])
            self.db.commit()
            result = True
        dlg.Destroy()
        self.load()
        return result

    def setup_config(self):
        """Create tables for this module."""
        for table, rows in DEFAULT_DATA.items():
            rows.extend([line for lst in updates.SETTINGS["settings"].values() for line in lst])
        self.db.setup(tables.SETTINGS, tables.get_columns_names, DEFAULT_DATA)


DEFAULT_DATA = {
    "settings": [
        '1, "donate_url", "https://privatbank.ua/sendmoney?payment=238a49dc4f28672ee467e18c5005cdc6287ac5d9"',
        '2, "general_language", "ru"',
        '3, "general_expand", "true"'
    ],
}


def load(data):
    """Construct class from json data."""
    temp_class_1 = type('__TempClass', (), {})
    temp_object = temp_class_1()
    for name, data_section in data.items():
        temp_class_2 = type('__' + name, (), {})
        setattr(temp_object, name, temp_class_2())
        section = getattr(temp_object, name)
        for key, value in data_section.items():
            value = __sub_load(value)
            setattr(section, key, value)

    return temp_object


def __sub_load(value):
    """Sub function for load json data to class structures."""
    __temp_class = type('__TempClass', (), {})
    __temp_object = __temp_class()
    if isinstance(value, dict):
        for key, item in value.items():
            item = __sub_load(item)
            setattr(__temp_object, key, item)
            value = __temp_object
    return value
