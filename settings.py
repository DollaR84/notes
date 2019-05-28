"""
Settings module.

Created on 25.05.2019

@author: Ruslan Dolovanyuk

"""

from wxdb import WXDB


class Settings(WXDB):
    """Settings program in database."""

    def __init__(self):
        """Initialization settings class."""
        super().__init__(self.__class__.__name__.lower())
        self.name = 'notes'
