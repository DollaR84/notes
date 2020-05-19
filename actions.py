"""
Algorithms actions module.

Created on 17.05.2020

@author: Ruslan Dolovanyuk

"""

import abc


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


class CreateNote(BaseAction):
    """Action for creating note in database."""

    def __init__(self, index, title):
        """Initialization action."""
        super().__init__(index)
        self.__title = title

    def run(self, tree, notes):
        """Running action."""
        parent_id = tree.get_parent_id(self.index)
        order = tree.get_count_childs(parent_id) + 1
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
