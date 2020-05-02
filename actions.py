"""
Algorithms actions module.

Created on 21.04.2020

@author: Ruslan Dolovanyuk

"""

import abc


class Starter:
    """Main central class for running algorithms."""

    def __init__(self, tree, notes):
        """Initialization central class."""
        self.__tree = tree
        self.__notes = notes

    def run(self, action):
        """Running method for actions."""
        action.run(self.__tree, self.__notes)


class BaseAction(abc.ABC):
    """Base class for all actions."""

    def __init__(self, index):
        """Initialization action.

        index: id current item for order;

        """
        self.index = index

    @abc.abstractmethod
    def run(self, tree, notes):
        """Run action need overload."""
        pass


class OrderUp(BaseAction):
    """Action order up item among parent childs."""

    def run(self, tree, notes):
        """Running action."""
        parent = tree.get_parent_id(self.index)
        order_dict = notes.get_order(parent)
        items = {}
        if order_dict[self.index] != 1:
            for key, value in order_dict.items():
                if value == order_dict[self.index] - 1:
                    if tree.get_count_childs(key) != 0:
                        items[self.index] = (key, tree.get_count_childs(key) + 1)
                        position_old = order_dict[self.index]
                        order_dict.pop(self.index)
                        for key, value in order_dict.items():
                            if value > position_old:
                                items[key] = (parent, value - 1)
                    else:
                        items[key] = (parent, value + 1)
                        items[self.index] = (parent, order_dict[self.index] - 1)
                    break
        else:
            parent_parent = tree.get_parent_id(parent)
            if parent_parent != -1:
                order_dict_parent = notes.get_order(parent_parent)
                items[self.index] = (parent_parent, order_dict_parent[parent])
                order_dict.pop(self.index)
                for key, value in order_dict.items():
                    items[key] = (parent, value - 1)
                for key, value in order_dict_parent.items():
                    if value >= order_dict_parent[parent]:
                        items[key] = (parent_parent, value + 1)
        notes.update(items)


class OrderDown(BaseAction):
    """Action order down item among parent childs."""

    def run(self, tree, notes):
        """Running action."""
        parent = tree.get_parent_id(self.index)
        order_dict = notes.get_order(parent)
        items = {}
        if order_dict[self.index] != tree.get_count_childs(parent):
            for key, value in order_dict.items():
                if value == order_dict[self.index] + 1:
                    if tree.get_count_childs(key) != 0:
                        for key_old, value_old in order_dict.items():
                            if value_old > order_dict[self.index]:
                                items[key_old] = (parent, value_old - 1)
                        items[self.index] = (key, 1)
                        order_dict_new = notes.get_order(key)
                        for key_new, value_new in order_dict_new.items():
                            items[key_new] = (key, value_new + 1)
                    else:
                        items[key] = (parent, value - 1)
                        items[self.index] = (parent, order_dict[self.index] + 1)
                    break
        else:
            parent_parent = tree.get_parent_id(parent)
            if parent_parent != -1:
                order_dict = notes.get_order(parent_parent)
                for key, value in order_dict.items():
                    if value > order_dict[parent]:
                        items[key] = (parent_parent, value + 1)
                items[self.index] = (parent_parent, order_dict[parent] + 1)
        notes.update(items)


class SortTitle(BaseAction):
    """Action sort by titles parent childs."""

    def run(self, tree, notes):
        """Running action."""
        order_dict = notes.get_order(self.index)
        items = {}
        titles = {}
        for key in list(order_dict.keys()):
            titles[key] = notes.get_note(key)[0]
        order_id = [item[0] for item in sorted(list(titles.items()), key=lambda i: i[1])]
        for i, index in enumerate(order_id):
            items[index] = (self.index, i)
        notes.update(items)


class SortChildCountUp(BaseAction):
    """Action sort by count kids parent childs up."""

    def run(self, tree, notes):
        """Running action."""
        order_dict = notes.get_order(self.index)
        items = {}
        childs = {}
        for key in list(order_dict.keys()):
            childs[key] = tree.get_count_childs(key)
        order_id = [item[0] for item in sorted(list(childs.items()), key=lambda i: i[1])]
        for i, index in enumerate(order_id):
            items[index] = (self.index, i)
        notes.update(items)


class SortChildCountDown(BaseAction):
    """Action sort by count kids parent childs down."""

    def run(self, tree, notes):
        """Running action."""
        order_dict = notes.get_order(self.index)
        items = {}
        childs = {}
        for key in list(order_dict.keys()):
            childs[key] = tree.get_count_childs(key)
        order_id = list(reversed([item[0] for item in sorted(list(childs.items()), key=lambda i: i[1])]))
        for i, index in enumerate(order_id):
            items[index] = (self.index, i)
        notes.update(items)
