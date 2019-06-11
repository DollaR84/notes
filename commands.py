"""
Commands for graphical interface.

Created on 25.05.2019

@author: Ruslan Dolovanyuk

"""

from api import Notes

from dialogs.dialogs import About
from dialogs.dialogs import Message

from configs import Config

from tree import Tree


class Commands:
    """Helper class, contains command for bind events, menu and buttons."""

    def __init__(self, drawer):
        """Initialization commands class."""
        self.drawer = drawer
        self.message = Message(self.drawer)
        self.config = Config()
        self.notes = Notes(self.config)
        self.tree = Tree()

        self.set_window()

    def set_window(self):
        """Set size and position window from saving data."""
        self.drawer.SetPosition(self.config.get_pos())
        self.drawer.SetSize(self.config.get_size())
        self.drawer.Layout()

    def about(self, event):
        """Run about dialog."""
        About(self.drawer,
              'О программе...',
              'Заметки',
              '1.0',
              'Руслан Долованюк').ShowModal()

    def close(self, event):
        """Close event for button close."""
        self.drawer.Close(True)

    def close_window(self, event):
        """Close window event."""
        self.config.set_pos(self.drawer.GetScreenPosition())
        self.config.set_size(self.drawer.GetSize())
        self.config.close()
        self.drawer.Destroy()

    def init_tree(self):
        """Initialization tree widget."""
        titles = self.notes.get_titles()
        parents = self.notes.get_parents()
        wx_tree_id = self.drawer.tree.AddRoot(self.config.root)
        self.tree.add(0, -1, wx_tree_id)
        for index in range(1, len(titles)+1):
            title = titles[index]
            parent_wx_tree_id = self.tree.id2wx_tree_id(parents[index])
            wx_tree_id = self.drawer.tree.AppendItem(parent_wx_tree_id, title)
            self.tree.add(index, parents[index], wx_tree_id)

    def tree_select(self, event):
        """Change select item in tree."""
        index = self.tree.wx_tree_id2id(self.drawer.tree.GetFocusedItem())
        if index == 0:
            self.drawer.but_del.Disable()
            self.drawer.title.SetValue('')
            self.drawer.data.SetValue('')
            self.drawer.title.Disable()
            self.drawer.data.Disable()
        else:
            self.drawer.but_del.Enable()
            self.drawer.title.Enable()
            self.drawer.data.Enable()
            title, data = self.notes.get_note(index)
            self.drawer.title.SetValue(title)
            self.drawer.data.SetValue(data)
        self.drawer.but_save.Disable()

    def text_change(self, event):
        """Change text controls note."""
        index = self.tree.wx_tree_id2id(self.drawer.tree.GetFocusedItem())
        if index != 0:
            self.drawer.but_save.Enable()

    def save(self, event):
        """Save note in database."""
        wx_tree_id = self.drawer.tree.GetFocusedItem()
        index = self.tree.wx_tree_id2id(wx_tree_id)
        title = self.drawer.title.GetValue()
        data = self.drawer.data.GetValue()
        self.notes.save(index, title, data)
        self.drawer.tree.SetItemText(wx_tree_id, title)

    def delete(self, event):
        """Delete note from database."""
        pass

    def create(self, event):
        """Create new note."""
        if event.GetId() == self.drawer.create_root.GetId():
            parent_id = 0
        else:
            parent_id = self.tree.wx_tree_id2id(self.drawer.tree.GetFocusedItem())
        index = self.tree.get_count()
        self.notes.create(index, parent_id)
        parent_wx_tree_id = self.tree.id2wx_tree_id(parent_id)
        wx_tree_id = self.drawer.tree.AppendItem(parent_wx_tree_id, 'Новая заметка')
        self.drawer.tree.Expand(parent_wx_tree_id)
        self.drawer.tree.SetFocusedItem(wx_tree_id)
        self.tree.add(index, parent_id, wx_tree_id)
        self.drawer.title.SetValue('Новая заметка')
        self.drawer.but_save.Disable()

    def count(self, event):
        """Show information of count notes."""
        object = event.GetEventObject()

    def options(self, event):
        """Run settings dialog."""
        self.config.open_settings(self.drawer)
