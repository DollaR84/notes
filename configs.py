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

    def get_states(self, states_default):
        """Return list states."""
        states = ['']
        states.extend(states_default)
        states.extend(self.get_user_states())
        return states

    def get_user_states(self):
        """Return list user states."""
        script = 'SELECT * FROM states'
        data = self.db.get(script)
        return [row[1] for row in data]

    def save_user_states(self, states):
        """Save list user states to database."""
        script = 'DELETE FROM states'
        self.db.put(script)
        for index, state in enumerate(states, 1):
            script = '''INSERT INTO states (id, state)
                        VALUES (?, ?)'''
            self.db.put(script, index, state)
        self.db.commit()

    def open_settings(self, parent):
        """Open settings dialog."""
        result = False
        dlg = SettingsDialog(parent, self)
        if RetCode.OK == dlg.ShowModal():
            dlg.config.pop('donate_url')
            dlg.config.pop('languages')
            self.save_user_states(dlg.config.pop('states'))
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
        tables_dict, default_data = updates.update(tables.SETTINGS, DEFAULT_DATA)
        self.db.setup(tables_dict, tables.get_columns_names, default_data)


DEFAULT_DATA = {
    "settings": [
        '1, "donate_url", "https://privatbank.ua/sendmoney?payment=238a49dc4f28672ee467e18c5005cdc6287ac5d9"',
        '2, "general_language", "ru"',
        '3, "general_expand", "true"'
    ],
    "states": [
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
