"""
Base algorithms actions module.

Created on 21.04.2020

@author: Ruslan Dolovanyuk

"""

import abc


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
