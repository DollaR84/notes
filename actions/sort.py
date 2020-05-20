"""
Sort algorithms actions module.

Created on 21.04.2020

@author: Ruslan Dolovanyuk

"""

from actions.base import BaseAction


class SortTitle(BaseAction):
    """Action sort by titles parent childs."""

    def run(self, tree, notes):
        """Running action."""
        self.__order_dict = notes.get_order(self.index)
        items = {}
        titles = {}
        for key in list(self.__order_dict.keys()):
            titles[key] = notes.get_note(key)[0]
        order_id = [item[0] for item in sorted(list(titles.items()), key=lambda i: i[1])]
        for i, index in enumerate(order_id, 1):
            items[index] = (self.index, i)
        notes.update(items)

    def undo(self, tree, notes):
        """Run undo action."""
        items = {index: (self.index, order_sort) for index, order_sort in self.__order_dict.items()}
        notes.update(items)


class SortChildCountUp(BaseAction):
    """Action sort by count kids parent childs up."""

    def run(self, tree, notes):
        """Running action."""
        self.__order_dict = notes.get_order(self.index)
        items = {}
        childs = {}
        for key in list(self.__order_dict.keys()):
            childs[key] = tree.get_count_childs(key)
        order_id = [item[0] for item in sorted(list(childs.items()), key=lambda i: i[1])]
        for i, index in enumerate(order_id, 1):
            items[index] = (self.index, i)
        notes.update(items)

    def undo(self, tree, notes):
        """Run undo action."""
        items = {index: (self.index, order_sort) for index, order_sort in self.__order_dict.items()}
        notes.update(items)


class SortChildCountDown(BaseAction):
    """Action sort by count kids parent childs down."""

    def run(self, tree, notes):
        """Running action."""
        self.__order_dict = notes.get_order(self.index)
        items = {}
        childs = {}
        for key in list(self.__order_dict.keys()):
            childs[key] = tree.get_count_childs(key)
        order_id = list(reversed([item[0] for item in sorted(list(childs.items()), key=lambda i: i[1])]))
        for i, index in enumerate(order_id, 1):
            items[index] = (self.index, i)
        notes.update(items)

    def undo(self, tree, notes):
        """Run undo action."""
        items = {index: (self.index, order_sort) for index, order_sort in self.__order_dict.items()}
        notes.update(items)
