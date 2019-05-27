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
        self.name = 'notes'
        super().__init__(self.name)
