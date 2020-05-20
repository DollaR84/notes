"""
Order algorithms actions module.

Created on 21.04.2020

@author: Ruslan Dolovanyuk

"""

from actions.base import BaseAction


class OrderUp(BaseAction):
    """Action order up item among parent childs."""

    def run(self, tree, notes):
        """Running action."""
        parent_id = tree.get_parent_id(self.index)
        order_dict = notes.get_order(parent_id)
        items = {}
        if order_dict[self.index] != 1:
            for key, value in order_dict.items():
                if value == order_dict[self.index] - 1:
                    items[key] = (parent_id, value + 1)
                    items[self.index] = (parent_id, order_dict[self.index] - 1)
                    break
        notes.update(items)

    def undo(self, tree, notes):
        """Run undo action."""
        action = OrderDown(self.index)
        action.run(tree, notes)


class OrderDown(BaseAction):
    """Action order down item among parent childs."""

    def run(self, tree, notes):
        """Running action."""
        parent_id = tree.get_parent_id(self.index)
        order_dict = notes.get_order(parent_id)
        items = {}
        if order_dict[self.index] != tree.get_count_childs(parent_id):
            for key, value in order_dict.items():
                if value == order_dict[self.index] + 1:
                    items[key] = (parent_id, value - 1)
                    items[self.index] = (parent_id, order_dict[self.index] + 1)
                    break
        notes.update(items)

    def undo(self, tree, notes):
        """Run undo action."""
        action = OrderUp(self.index)
        action.run(tree, notes)


class OrderParentUp(BaseAction):
    """Action order up item change parent."""

    def run(self, tree, notes):
        """Running action."""
        parent_id = tree.get_parent_id(self.index)
        order_dict = notes.get_order(parent_id)
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
                                items[key] = (parent_id, value - 1)
                    else:
                        items[self.index] = (key, 1)
                        position_old = order_dict[self.index]
                        order_dict.pop(self.index)
                        for key, value in order_dict.items():
                            if value > position_old:
                                items[key] = (parent_id, value - 1)
                    break
        else:
            parent_parent = tree.get_parent_id(parent_id)
            if parent_parent != -1:
                order_dict_parent = notes.get_order(parent_parent)
                items[self.index] = (parent_parent, order_dict_parent[parent_id])
                order_dict.pop(self.index)
                for key, value in order_dict.items():
                    items[key] = (parent_id, value - 1)
                for key, value in order_dict_parent.items():
                    if value >= order_dict_parent[parent_id]:
                        items[key] = (parent_parent, value + 1)
        notes.update(items)

    def undo(self, tree, notes):
        """Run undo action."""
        action = OrderParentDown(self.index)
        action.run(tree, notes)


class OrderParentDown(BaseAction):
    """Action order down item among parent childs."""

    def run(self, tree, notes):
        """Running action."""
        parent_id = tree.get_parent_id(self.index)
        order_dict = notes.get_order(parent_id)
        items = {}
        if order_dict[self.index] != tree.get_count_childs(parent_id):
            for key, value in order_dict.items():
                if value == order_dict[self.index] + 1:
                    if tree.get_count_childs(key) != 0:
                        for key_old, value_old in order_dict.items():
                            if value_old > order_dict[self.index]:
                                items[key_old] = (parent_id, value_old - 1)
                        items[self.index] = (key, 1)
                        order_dict_new = notes.get_order(key)
                        for key_new, value_new in order_dict_new.items():
                            items[key_new] = (key, value_new + 1)
                    else:
                        items[self.index] = (key, 1)
                        position_old = order_dict[self.index]
                        order_dict.pop(self.index)
                        for key, value in order_dict.items():
                            if value > position_old:
                                items[key] = (parent_id, value - 1)
                    break
        else:
            parent_parent = tree.get_parent_id(parent_id)
            if parent_parent != -1:
                order_dict = notes.get_order(parent_parent)
                for key, value in order_dict.items():
                    if value > order_dict[parent_id]:
                        items[key] = (parent_parent, value + 1)
                items[self.index] = (parent_parent, order_dict[parent_id] + 1)
        notes.update(items)

    def undo(self, tree, notes):
        """Run undo action."""
        action = OrderParentUp(self.index)
        action.run(tree, notes)
