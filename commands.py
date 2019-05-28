"""
Commands for graphical interface.

Created on 25.05.2019

@author: Ruslan Dolovanyuk

"""

from dialogs import About
from dialogs import Message

from settings import Settings


class Commands:
    """Helper class, contains command for bind events, menu and buttons."""

    def __init__(self, drawer):
        """Initialization commands class."""
        self.drawer = drawer
        self.message = Message(self.drawer)
        self.settings = Settings()

        self.set_window()

    def set_window(self):
        """Set size and position window from saving data."""
        self.drawer.SetPosition(self.settings.get_pos())
        self.drawer.SetSize(self.settings.get_size())
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
        self.settings.set_pos(self.drawer.GetScreenPosition())
        self.settings.set_size(self.drawer.GetSize())
        self.settings.finish()
        self.drawer.Destroy()