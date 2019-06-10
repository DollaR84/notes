"""
Tree module for notes.

Created on 08.06.2019

@author: Ruslan Dolovanyuk

"""


class Item:
    """Item class for tree."""

    def __init__(self, index, parent_id, wx_tree_id):
        """Initialization item for tree."""
        self.id = index
        self.parent_id = parent_id
        self.wx_tree_id = wx_tree_id


class Tree:
    """Tree class for notes."""

    def __init__(self):
        """Initialization tree class for notes."""
        self.__elements = []

    def add(self, index, parent_id, wx_tree_id):
        """Add item in list."""
        self.__elements.append(Item(index, parent_id, wx_tree_id))

    def id2wx_tree_id(self, index):
        """Return wx_tree_id from incoming id."""
        for element in self.__elements:
            if element.id == index:
                return element.wx_tree_id

    def wx_tree_id2id(self, wx_tree_id):
        """Return id from incoming wx_tree_id."""
        for element in self.__elements:
            if element.wx_tree_id == wx_tree_id:
                return element.id

    def get_count(self):
        """Return count elements in tree."""
        return len(self.__elements)

    def get_parent_id(self, index):
        """Return parent id for incoming item."""
        return self.__elements[index].parent_id
