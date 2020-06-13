"""
Extend algorithms actions module.

Created on 13.06.2020

@author: Ruslan Dolovanyuk

"""

from actions.base import BaseAction


class SetReadonly(BaseAction):
    """Action for set readonly attribute on note."""

    def __init__(self, index, readonly):
        """Initialization action."""
        super().__init__(index)
        self.__readonly = readonly

    def run(self, tree, notes):
        """Running action."""
        notes.save_readonly(self.index, self.__readonly)

    def undo(self, tree, notes):
        """Undo action."""
        notes.save_readonly(self.index, not self.__readonly)


class SetStateCheck(BaseAction):
    """Action for set state_check attribute on note."""

    def __init__(self, index, state):
        """Initialization action."""
        super().__init__(index)
        self.__state = state

    def run(self, tree, notes):
        """Running action."""
        notes.save_state_check(self.index, self.__state)

    def undo(self, tree, notes):
        """Undo action."""
        notes.save_state_check(self.index, not self.__state)


class SetState(BaseAction):
    """Action for set state string on note."""

    def __init__(self, index, state):
        """Initialization action."""
        super().__init__(index)
        self.__new = state

    def run(self, tree, notes):
        """Running action."""
        self.__old = notes.get_state(self.index)
        notes.save_state(self.index, self.__new)

    def undo(self, tree, notes):
        """Undo action."""
        action = SetState(self.index, self.__old)
        action.run(tree, notes)
