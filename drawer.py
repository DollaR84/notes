"""
Graphical form for notes.

Created on 25.05.2019

@author: Ruslan Dolovanyuk

"""

from accessible import TreeAccessible

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
        self.phrases = configs.load(self.config.get_language(self.config.general_language))
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
        self.readonly.Disable()
        self.state_check.Disable()
        self.states.Disable()

    def __create_widgets(self):
        """Create widgets program."""
        self.tree = wx.TreeCtrl(self.panel, wx.ID_ANY,
                                style=wx.TR_DEFAULT_STYLE |
                                wx.TR_SINGLE |
                                wx.TR_LINES_AT_ROOT |
                                wx.TR_TWIST_BUTTONS |
                                wx.TR_EDIT_LABELS)
        self.tree.SetAccessible(TreeAccessible(self))
        box_note = wx.StaticBox(self.panel, wx.ID_ANY, self.phrases.widgets.box_note)
        self.data = wx.TextCtrl(box_note, wx.ID_ANY, style=wx.TE_MULTILINE)
        self.data.SetBackgroundColour('Yellow')
        self.readonly = wx.CheckBox(self.panel, wx.ID_ANY, self.phrases.widgets.readonly)
        box_state = wx.StaticBox(self.panel, wx.ID_ANY, self.phrases.widgets.box_state)
        self.state_check = wx.CheckBox(box_state, wx.ID_ANY, self.phrases.widgets.state_check)
        self.states = wx.Choice(box_state, wx.ID_ANY, choices=self.config.get_states(self.phrases.widgets.states))
        self.but_save = wx.Button(self.panel, wx.ID_ANY, self.phrases.widgets.but_save)
        self.but_del = wx.Button(self.panel, wx.ID_ANY, self.phrases.widgets.but_del)
        self.but_create = wx.Button(self.panel, wx.ID_ANY, self.phrases.widgets.but_create)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.Add(self.tree, 1, wx.EXPAND | wx.ALL, 5)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        box_note_sizer = wx.StaticBoxSizer(box_note, wx.HORIZONTAL)
        box_note_sizer.Add(self.data, 1, wx.EXPAND | wx.ALL, 5)
        right_sizer.Add(box_note_sizer, 1, wx.EXPAND | wx.ALL)
        right_sizer.Add(self.readonly, 0, wx.EXPAND | wx.ALL | wx.ALIGN_LEFT, 5)
        state_sizer = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        state_sizer.Add(self.state_check, 1, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        state_sizer.Add(self.states, 1, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        right_sizer.Add(state_sizer, 0, wx.EXPAND | wx.ALL)
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
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, getattr(self.command, 'tree_activated'), self.tree)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, getattr(self.command, 'tree_end_edit'), self.tree)
        self.Bind(wx.EVT_TEXT, getattr(self.command, 'text_change'), self.data)
        self.Bind(wx.EVT_CHECKBOX, getattr(self.command, 'change_readonly'), self.readonly)
        self.Bind(wx.EVT_CHECKBOX, getattr(self.command, 'change_state'), self.state_check)
        self.Bind(wx.EVT_CHOICE, getattr(self.command, 'choice_state'), self.states)
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'save'), self.but_save)
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'delete'), self.but_del)
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'create'), self.but_create)

    def get_not_found(self):
        """Return wx.NOT_FOUND value."""
        return wx.NOT_FOUND
