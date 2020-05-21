"""
Main running algorithms actions module.

Created on 21.04.2020

@author: Ruslan Dolovanyuk

"""

from actions.base import BaseAction


class CreateNote(BaseAction):
    """Action for creating note in database."""

    def __init__(self, index, title):
        """Initialization action."""
        super().__init__(index)
        self.__title = title

    def run(self, tree, notes):
        """Running action."""
        parent_id = tree.get_parent_id(self.index)
        order = tree.get_count_childs(parent_id)
        notes.create(self.index, self.__title, parent_id, order)

    def undo(self, tree, notes):
        """Undo action."""
        action = DelNote(self.index)
        action.run(tree, notes)


class InsertNote(BaseAction):
    """Action for insert note in database."""

    def __init__(self, index, before_item, title):
        """Initialization action."""
        super().__init__(index)
        self.__before_item = before_item
        self.__title = title

    def run(self, tree, notes):
        """Running action."""
        parent_id = tree.get_parent_id(self.__before_item)
        order_dict = notes.get_order(parent_id)
        order = order_dict[self.__before_item] + 1
        items = {index: (parent_id, order_sort+1) for index, order_sort in order_dict.items() if order_sort > order_dict[self.__before_item]}
        notes.create(self.index, self.__title, parent_id, order)
        notes.update(items)

    def undo(self, tree, notes):
        """Undo action."""
        action = DelNote(self.index)
        action.run(tree, notes)


class SaveTitle(BaseAction):
    """Action for saving title note in database."""

    def __init__(self, index, title):
        """Initialization saving title note to database."""
        super().__init__(index)
        self.__new = title

    def run(self, tree, notes):
        """Running action."""
        self.__old = notes.get_title(self.index)
        notes.save_title(self.index, self.__new)

    def undo(self, tree, notes):
        """Undo action."""
        action = SaveTitle(self.index, self.__old)
        action.run(tree, notes)


class SaveNote(BaseAction):
    """Action for saving data note in database."""

    def __init__(self, index, data):
        """Initialization saving data note to database."""
        super().__init__(index)
        self.__new = data

    def run(self, tree, notes):
        """Running action."""
        self.__old = notes.get_note(self.index)
        notes.save_note(self.index, self.__new)

    def undo(self, tree, notes):
        """Undo action."""
        action = SaveNote(self.index, self.__old)
        action.run(tree, notes)


class DelNote(BaseAction):
    """Action for deleting note from database."""

    def run(self, tree, notes):
        """Running action."""
        self.__parent_id = tree.get_parent_id(self.index)
        self.__order = notes.get_order(self.__parent_id)[self.index]
        self.__title = notes.get_title(self.index)
        self.__data = notes.get_note(self.index)
        notes.del_note(self.index)

    def undo(self, tree, notes):
        """Run undo action."""
        index = tree.get_count()
        order_dict = notes.get_order(self.__parent_id)
        items = {idx: (self.__parent_id, order_sort+1) for idx, order_sort in order_dict.items() if order_sort >= self.__order}
        notes.create(index, self.__title, self.__parent_id, self.__order)
        notes.update(items)
        notes.save_note(index, self.__data)
