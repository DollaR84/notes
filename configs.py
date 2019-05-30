"""
Configs module.

Created on 25.05.2019

@author: Ruslan Dolovanyuk

"""

from dialogs.dialogs import RetCode

from dialogs.settings import SettingsDialog

from wxdb import WXDB


class Config(WXDB):
    """Config program in database."""

    def __init__(self):
        """Initialization config class."""
        super().__init__(self.__class__.__name__.lower())
        self.name = 'notes'
