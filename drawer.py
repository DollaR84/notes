"""
Graphical form for notes.

Created on 25.05.2019

@author: Ruslan Dolovanyuk

"""

import pickle

from commands import Commands

import configs

from menu import Menu

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
        self.config = configs.Config()
        with open('languages.dat', 'rb') as lang_file:
            lang_dict = pickle.load(lang_file)
            self.config.set_languages(lang_dict['languages'])
            self.phrases = configs.load(lang_dict[self.config.general_language])
        super().__init__(None, wx.ID_ANY, self.phrases.titles.caption)
        self.command = Commands(self)
        self.menu = Menu(self)

        self.panel = wx.Panel(self, wx.ID_ANY)
        sizer_panel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_panel.Add(self.panel, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer_panel)

        self.CreateStatusBar()
        self.__create_widgets()
        self.__create_bindings()

        self.command.init_tree()
        self.but_save.Disable()
        self.but_del.Disable()

    def __create_widgets(self):
        """Create widgets program."""
        self.tree = wx.TreeCtrl(self.panel, wx.ID_ANY,
                                style=wx.TR_DEFAULT_STYLE |
                                wx.TR_SINGLE |
                                wx.TR_LINES_AT_ROOT |
                                wx.TR_HAS_BUTTONS)
        box_title = wx.StaticBox(self.panel, wx.ID_ANY, self.phrases.widgets.box_title)
        self.title = wx.TextCtrl(box_title, wx.ID_ANY)
        box_data = wx.StaticBox(self.panel, wx.ID_ANY, self.phrases.widgets.box_data)
        self.data = wx.TextCtrl(box_data, wx.ID_ANY, style=wx.TE_MULTILINE)
        self.but_save = wx.Button(self.panel, wx.ID_ANY, self.phrases.widgets.but_save)
        self.but_del = wx.Button(self.panel, wx.ID_ANY, self.phrases.widgets.but_del)
        self.but_create = wx.Button(self.panel, wx.ID_ANY, self.phrases.widgets.but_create)

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
        but_sizer = wx.GridSizer(rows=1, cols=3, hgap=5, vgap=5)
        but_sizer.Add(self.but_save, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        but_sizer.Add(self.but_del, 0, wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL)
        but_sizer.Add(self.but_create, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        right_sizer.Add(but_sizer, 0, wx.EXPAND | wx.ALL)
        sizer.Add(left_sizer, 0, wx.EXPAND | wx.ALL)
        sizer.Add(right_sizer, 1, wx.EXPAND | wx.ALL)
        self.panel.SetSizer(sizer)

    def __create_bindings(self):
        """Create bindings for widgets and other events."""
        self.Bind(wx.EVT_CLOSE, getattr(self.command, 'close_window'))
        self.Bind(wx.EVT_TREE_SEL_CHANGED, getattr(self.command, 'tree_select'), self.tree)
        self.Bind(wx.EVT_TEXT, getattr(self.command, 'text_change'), self.title)
        self.Bind(wx.EVT_TEXT, getattr(self.command, 'text_change'), self.data)
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'save'), self.but_save)
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'delete'), self.but_del)
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'create'), self.but_create)
