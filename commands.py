"""
Commands for graphical interface.

Created on 25.05.2019

@author: Ruslan Dolovanyuk

"""

from collections import OrderedDict

import webbrowser

from actions import Starter
from actions import OrderUp, OrderDown
from actions import SortTitle, SortChildCountUp, SortChildCountDown

from api import Notes

from dialogs.dialogs import About
from dialogs.dialogs import Message

from tree import Tree

import version


class Commands:
    """Helper class, contains command for bind events, menu and buttons."""

    def __init__(self, drawer):
        """Initialization commands class."""
        self.drawer = drawer
        self.phrases = self.drawer.phrases
        self.config = self.drawer.config
        self.message = Message(self.drawer)
        self.notes = Notes(self.message, self.phrases)
        self.tree = Tree()
        self.starter = Starter(self.tree, self.notes)

        self.set_window()

    def set_window(self):
        """Set size and position window from saving data."""
        self.drawer.SetPosition(self.config.get_pos())
        self.drawer.SetSize(self.config.get_size())
        self.drawer.Layout()

    def donate(self, event):
        """Run donate hyperlink in browser."""
        webbrowser.open(self.config.donate_url)

    def home(self, event):
        """Run home page hyperlink in browser."""
        webbrowser.open(self.phrases.about.url)

    def about(self, event):
        """Run about dialog."""
        About(
              self.drawer,
              self.phrases.about.title,
              self.phrases.about.name,
              version.VERSION,
              self.phrases.about.author
             ).ShowModal()

    def close(self, event):
        """Close event for button close."""
        self.drawer.Close(True)

    def close_window(self, event):
        """Close window event."""
        if self.config.general_expand == 'true':
            self.expand_tree_save()
        self.notes.close()

        self.config.set_pos(self.drawer.GetScreenPosition())
        self.config.set_size(self.drawer.GetSize())
        self.config.close()

        self.drawer.Destroy()

    def __sort(self, titles, parents):
        """Sort titles and parents dictionaries by order_sort field."""
        order_titles = OrderedDict()
        order_parents = OrderedDict()
        parents_unique = {}
        for key, value in parents.items():
            if value not in parents_unique:
                parents_unique[value] = []
            parents_unique[value].append(key)
        parents_unique_keys = sorted(list(parents_unique.keys()))
        for parent in parents_unique_keys:
            childs = parents_unique[parent]
            order_dict = self.notes.get_order(parent)
            order_id = [item[0] for item in sorted(list(order_dict.items()), key=lambda i: i[1])]
            for index in order_id:
                order_titles[index] = titles[index]
                order_parents[index] = parents[index]
        return order_titles, order_parents

    def init_tree(self):
        """Initialization tree widget."""
        titles = self.notes.get_titles()
        parents = self.notes.get_parents()
        titles, parents = self.__sort(titles, parents)
        wx_tree_id = self.drawer.tree.AddRoot(self.phrases.widgets.tree.root)
        self.tree.add(0, -1, wx_tree_id)
        for index, title in titles.items():
            parent_wx_tree_id = self.tree.id2wx_tree_id(parents[index])
            wx_tree_id = self.drawer.tree.AppendItem(parent_wx_tree_id, title)
            self.tree.add(index, parents[index], wx_tree_id)
        if self.config.general_expand == 'true':
            self.expand_tree_init()

    def expand_tree_init(self):
        """Init expand tree if set config settings."""
        expands = self.notes.get_expands()
        wx_tree_id = self.tree.id2wx_tree_id(0)
        self.drawer.tree.Expand(wx_tree_id)
        for index in range(1, self.tree.get_count()):
            wx_tree_id = self.tree.id2wx_tree_id(index)
            if expands.get(index, 0) == 1:
                self.drawer.tree.Expand(wx_tree_id)
            else:
                self.drawer.tree.Collapse(wx_tree_id)

    def expand_tree_save(self):
        """Save expand tree if set config settings."""
        expands = {}
        for index in range(1, self.tree.get_count()):
            wx_tree_id = self.tree.id2wx_tree_id(index)
            if self.drawer.tree.IsExpanded(wx_tree_id):
                expands[index] = 1
            else:
                expands[index] = 0
        self.notes.set_expands(expands)

    def __set_state_order_menuitem(self, state):
        """Set state menu items order."""
        self.drawer.order_up.Enable(state)
        self.drawer.order_down.Enable(state)

    def __set_state_sort_menuitem(self, state):
        """Set state menu items sort."""
        self.drawer.sort_titles.Enable(state)
        self.drawer.sort_childcount_up.Enable(state)
        self.drawer.sort_childcount_down.Enable(state)

    def tree_select(self, event):
        """Change select item in tree."""
        index = self.tree.wx_tree_id2id(self.drawer.tree.GetSelection())
        if index is None:
            self.__set_state_order_menuitem(False)
            self.__set_state_sort_menuitem(False)
        elif index == 0:
            self.__set_state_order_menuitem(False)
            self.__set_state_sort_menuitem(True)
            self.drawer.but_del.Disable()
            self.drawer.del_note.Enable(False)
            self.drawer.title.SetValue('')
            self.drawer.data.SetValue('')
            self.drawer.title.Disable()
            self.drawer.data.Disable()
        else:
            self.__set_state_order_menuitem(True)
            self.__set_state_sort_menuitem(True)
            self.drawer.but_del.Enable()
            self.drawer.del_note.Enable(True)
            self.drawer.title.Enable()
            self.drawer.data.Enable()
            title, data = self.notes.get_note(index)
            self.drawer.title.SetValue(title)
            self.drawer.data.SetValue(data)
        self.drawer.but_save.Disable()
        self.drawer.save_note.Enable(False)

    def text_change(self, event):
        """Change text controls note."""
        index = self.tree.wx_tree_id2id(self.drawer.tree.GetSelection())
        if index != 0:
            self.drawer.but_save.Enable()
            self.drawer.save_note.Enable(True)

    def save(self, event):
        """Save note in database."""
        wx_tree_id = self.drawer.tree.GetSelection()
        index = self.tree.wx_tree_id2id(wx_tree_id)
        title = self.drawer.title.GetValue()
        data = self.drawer.data.GetValue()
        self.notes.save(index, title, data)
        self.drawer.tree.SetItemText(wx_tree_id, title)
        self.drawer.but_save.Disable()
        self.drawer.save_note.Enable(False)

    def delete(self, event):
        """Delete note from database."""
        if self.message.question(self.phrases.titles.warning, self.phrases.questions.del_note):
            index = self.tree.wx_tree_id2id(self.drawer.tree.GetSelection())
            parent_id = self.tree.get_parent_id(index)
            self.drawer.tree.DeleteAllItems()
            self.notes.del_note(index)
            self.tree.clear()
            self.init_tree()
            self.drawer.tree.SelectItem(self.tree.id2wx_tree_id(parent_id))

    def create(self, event):
        """Create new note."""
        if event.GetId() == self.drawer.create_root.GetId():
            parent_id = 0
        else:
            parent_id = self.tree.wx_tree_id2id(self.drawer.tree.GetSelection())
        index = self.tree.get_count()
        order_sort = self.tree.get_count_childs()
        self.notes.create(index, parent_id, order_sort)
        parent_wx_tree_id = self.tree.id2wx_tree_id(parent_id)
        wx_tree_id = self.drawer.tree.AppendItem(parent_wx_tree_id, self.phrases.widgets.tree.new_note)
        self.drawer.tree.Expand(parent_wx_tree_id)
        self.drawer.tree.SelectItem(wx_tree_id)
        self.tree.add(index, parent_id, wx_tree_id)
        if not self.drawer.title.IsEnabled():
            self.drawer.title.Enable()
        if not self.drawer.data.IsEnabled():
            self.drawer.data.Enable()
        self.drawer.title.SetValue(self.phrases.widgets.new_title)
        self.drawer.data.SetValue('')

    def order(self, event):
        """Order items."""
        index = self.tree.wx_tree_id2id(self.drawer.tree.GetSelection())
        if event.GetId() == self.drawer.order_up.GetId():
            self.starter.run(OrderUp(index))
        elif event.GetId() == self.drawer.order_down.GetId():
            self.starter.run(OrderDown(index))
        self.expand_tree_save()
        self.tree.clear()
        self.drawer.tree.DeleteAllItems()
        self.init_tree()
        self.drawer.tree.SelectItem(self.tree.id2wx_tree_id(index))

    def sort(self, event):
        """Sort items."""
        index = self.tree.wx_tree_id2id(self.drawer.tree.GetSelection())
        if event.GetId() == self.drawer.sort_titles.GetId():
            self.starter.run(SortTitle(index))
        elif event.GetId() == self.drawer.sort_childcount_up.GetId():
            self.starter.run(SortChildCountUp(index))
        elif event.GetId() == self.drawer.sort_childcount_down.GetId():
            self.starter.run(SortChildCountDown(index))
        self.expand_tree_save()
        self.tree.clear()
        self.drawer.tree.DeleteAllItems()
        self.init_tree()
        self.drawer.tree.SelectItem(self.tree.id2wx_tree_id(index))

    def count(self, event):
        """Show information of count notes."""
        if event.GetId() == self.drawer.count_root.GetId():
            self.message.information(self.phrases.titles.info, self.phrases.count.root % self.tree.get_count_childs(0))
        elif event.GetId() == self.drawer.count_child.GetId():
            index = self.tree.wx_tree_id2id(self.drawer.tree.GetSelection())
            self.message.information(self.phrases.titles.info, self.phrases.count.child % self.tree.get_count_childs(index))
        else:
            self.message.information(self.phrases.titles.info, self.phrases.count.total % (self.tree.get_count() - 1))

    def options(self, event):
        """Run settings dialog."""
        self.config.open_settings(self.drawer)
