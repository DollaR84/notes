"""
Actions starting module.

Created on 17.05.2020

@author: Ruslan Dolovanyuk

"""

from actions.history import History


class Actions:
    """Main central class for running algorithms."""

    def __init__(self, tree, notes):
        """Initialization central class."""
        self.__tree = tree
        self.__notes = notes

        self.__history = History()

    def run(self, action):
        """Running method for actions."""
        action.run(self.__tree, self.__notes)
        self.__history.add(action)

    def undo(self):
        """Run undo operation."""
        self.__history.undo(self.__tree, self.__notes)

    def redo(self):
        """Run redo operation."""
        self.__history.redo(self.__tree, self.__notes)

    def isUndo(self):
        """Return state undo list."""
        return self.__history.isUndo()

    def isRedo(self):
        """Return state redo list."""
        return self.__history.isRedo()
