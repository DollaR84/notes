"""
Graphical form for notes.

Created on 25.05.2019

@author: Ruslan Dolovanyuk

"""

from commands import Commands

import wx


class Drawer:
    """Graphical form for notes."""

    def __init__(self):
        """Initialization drawer form."""
        self.app = wx.App()
        self.wnd = NotesFrame()
        self.wnd.Show(True)
        self.app.SetTopWindow(self.wnd)

    def mainloop(self):
        """Graphical main loop running."""
        self.app.MainLoop()


class NotesFrame(wx.Frame):
    """Create user interface."""

    def __init__(self):
        """Initialization interface."""
        super().__init__(None, wx.ID_ANY, 'Заметки')
        self.command = Commands(self)

        self.panel = wx.Panel(self, wx.ID_ANY)
        sizer_panel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_panel.Add(self.panel, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer_panel)

        self.CreateStatusBar()
        self.__create_menu()
        self.__create_widgets()
        self.__create_bindings()

    def __create_menu(self):
        """Create menu program."""
        pass

    def __create_widgets(self):
        """Create widgets program."""
        self.tree = wx.TreeCtrl(self.panel, wx.ID_ANY,
                                style=wx.TR_DEFAULT_STYLE |
                                      wx.TR_SINGLE |
                                      wx.TR_LINES_AT_ROOT |
                                      wx.TR_HAS_BUTTONS)
        box_title = wx.StaticBox(self.panel, wx.ID_ANY, 'Заголовок')
        self.title = wx.TextCtrl(box_title, wx.ID_ANY)
        box_data = wx.StaticBox(self.panel, wx.ID_ANY, 'Текст')
        self.data = wx.TextCtrl(box_data, wx.ID_ANY, style=wx.TE_MULTILINE)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.Add(self.tree, 1, wx.EXPAND | wx.ALL, 5)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        box_title_sizer = wx.StaticBoxSizer(box_title, wx.HORIZONTAL)
        box_title_sizer.Add(self.title, 1, wx.EXPAND | wx.ALL, 5)
        box_data_sizer = wx.StaticBoxSizer(box_data, wx.HORIZONTAL)
        box_data_sizer.Add(self.data, 1, wx.EXPAND | wx.ALL, 5)
        right_sizer.Add(box_title_sizer, 0, wx.EXPAND | wx.ALL)
        right_sizer.Add(box_data_sizer, 1, wx.EXPAND | wx.ALL)
        sizer.Add(left_sizer, 0, wx.EXPAND | wx.ALL)
        sizer.Add(right_sizer, 1, wx.EXPAND | wx.ALL)
        self.panel.SetSizer(sizer)

    def __create_bindings(self):
        """Create bindings for menu, widgets and other events."""
        pass
