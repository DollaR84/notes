"""
Commands for graphical interface.

Created on 25.05.2019

@author: Ruslan Dolovanyuk

"""

import webbrowser

from api import Notes

from dialogs.dialogs import About
from dialogs.dialogs import Message

from tree import Tree


class Commands:
    """Helper class, contains command for bind events, menu and buttons."""

    def __init__(self, drawer):
        """Initialization commands class."""
        self.drawer = drawer
        self.phrases = self.drawer.phrases
        self.config = self.drawer.config
        self.message = Message(self.drawer)
        self.notes = Notes(self.config)
        self.tree = Tree()

        self.set_window()

    def set_window(self):
        """Set size and position window from saving data."""
        self.drawer.SetPosition(self.config.get_pos())
        self.drawer.SetSize(self.config.get_size())
        self.drawer.Layout()

    def donate(self, event):
        """Run donate hyperlink in browser."""
        webbrowser.open(self.config.donate_url)

    def about(self, event):
        """Run about dialog."""
        About(
              self.drawer,
              self.phrases.about.title,
              self.phrases.about.name,
              self.phrases.about.version,
              self.phrases.about.author
             ).ShowModal()

    def close(self, event):
        """Close event for button close."""
        self.drawer.Close(True)

    def close_window(self, event):
        """Close window event."""
        if self.config.general_expand == 'true':
            self.expand_tree_save()
        self.config.set_pos(self.drawer.GetScreenPosition())
        self.config.set_size(self.drawer.GetSize())
        self.config.close()
        self.drawer.Destroy()

    def init_tree(self):
        """Initialization tree widget."""
        titles = self.notes.get_titles()
        parents = self.notes.get_parents()
        wx_tree_id = self.drawer.tree.AddRoot(self.phrases.widgets.tree.root)
        self.tree.add(0, -1, wx_tree_id)
        for index in range(1, len(titles) + 1):
            title = titles[index]
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

    def tree_select(self, event):
        """Change select item in tree."""
        index = self.tree.wx_tree_id2id(self.drawer.tree.GetFocusedItem())
        if index == 0:
            self.drawer.but_del.Disable()
            self.drawer.del_note.Enable(False)
            self.drawer.title.SetValue('')
            self.drawer.data.SetValue('')
            self.drawer.title.Disable()
            self.drawer.data.Disable()
        else:
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
        index = self.tree.wx_tree_id2id(self.drawer.tree.GetFocusedItem())
        if index != 0:
            self.drawer.but_save.Enable()
            self.drawer.save_note.Enable(True)

    def save(self, event):
        """Save note in database."""
        wx_tree_id = self.drawer.tree.GetFocusedItem()
        index = self.tree.wx_tree_id2id(wx_tree_id)
        title = self.drawer.title.GetValue()
        data = self.drawer.data.GetValue()
        self.notes.save(index, title, data)
        self.drawer.tree.SetItemText(wx_tree_id, title)
        self.drawer.but_save.Disable()
        self.drawer.save_note.Enable(False)

    def delete(self, event):
        """Delete note from database."""
        index = self.tree.wx_tree_id2id(self.drawer.tree.GetFocusedItem())
        parent_id = self.tree.get_parent_id(index)
        self.drawer.tree.DeleteAllItems()
        self.notes.del_note(index)
        self.tree.clear()
        self.init_tree()
        self.drawer.tree.SetFocusedItem(self.tree.id2wx_tree_id(parent_id))

    def create(self, event):
        """Create new note."""
        if event.GetId() == self.drawer.create_root.GetId():
            parent_id = 0
        else:
            parent_id = self.tree.wx_tree_id2id(self.drawer.tree.GetFocusedItem())
        index = self.tree.get_count()
        self.notes.create(index, parent_id)
        parent_wx_tree_id = self.tree.id2wx_tree_id(parent_id)
        wx_tree_id = self.drawer.tree.AppendItem(parent_wx_tree_id, self.phrases.widgets.tree.new_note)
        self.drawer.tree.Expand(parent_wx_tree_id)
        self.drawer.tree.SetFocusedItem(wx_tree_id)
        self.tree.add(index, parent_id, wx_tree_id)
        self.drawer.title.SetValue(self.phrases.widgets.new_title)
        self.drawer.but_save.Disable()
        self.drawer.save_note.Enable(False)

    def count(self, event):
        """Show information of count notes."""
        if event.GetId() == self.drawer.count_root.GetId():
            self.message.information(self.phrases.titles.info, self.phrases.count.root % self.tree.get_count_childs(0))
        elif event.GetId() == self.drawer.count_child.GetId():
            index = self.tree.wx_tree_id2id(self.drawer.tree.GetFocusedItem())
            self.message.information(self.phrases.titles.info, self.phrases.count.child % self.tree.get_count_childs(index))
        else:
            self.message.information(self.phrases.titles.info, self.phrases.count.total % (self.tree.get_count() - 1))

    def options(self, event):
        """Run settings dialog."""
        self.config.open_settings(self.drawer)
