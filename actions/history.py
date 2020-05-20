"""
history algorithms actions module.

Created on 19.05.2020

@author: Ruslan Dolovanyuk

"""


class History:
    """Class implements undo and redo operations."""

    def __init__(self):
        """Initialization class."""
        self.__undo_list = []
        self.__redo_list = []

    def add(self, action):
        """Add action in undo list."""
        self.__undo_list.append(action)

    def undo(self, tree, notes):
        """Run undo action."""
        if self.__undo_list:
            action = self.__undo_list.pop()
            action.undo(tree, notes)
            self.__redo_list.append(action)

    def redo(self, tree, notes):
        """Run redo action."""
        if self.__redo_list:
            action = self.__redo_list.pop()
            action.run(tree, notes)
            self.__undo_list.append(action)

    def isUndo(self):
        """Return state undo list."""
        return bool(self.__undo_list)

    def isRedo(self):
        """Return state redo list."""
        return bool(self.__redo_list)
