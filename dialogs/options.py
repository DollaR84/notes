"""
Graphic form change settings.

Created on 29.05.2019

@author: Ruslan Dolovanyuk

"""

import hashlib

from dialogs.dialogs import PasswordEntryDialog
from dialogs.dialogs import RetCode

import wx


class SettingsDialog(wx.Dialog):
    """Create interface settings dialog."""

    def __init__(self, parent, config):
        """Initialize interface."""
        super().__init__(parent, wx.ID_ANY, parent.phrases.settings.title)
        self.phrases = parent.phrases.settings
        self.config = {key: getattr(config, key) for key in config.ids.keys()}
        self.config['languages'] = config.get_languages()
        self.config['states'] = config.get_user_states()

        notebook = wx.Notebook(self, wx.ID_ANY)
        self.general = TabGeneral(notebook, parent, self.config, self.phrases.general)
        self.state = TabState(notebook, parent, self.config, self.phrases.state)
        self.speech = TabSpeech(notebook, parent, self.config, self.phrases.speech)

        notebook.AddPage(self.general, self.phrases.general.title)
        notebook.AddPage(self.state, self.phrases.state.title)
        notebook.AddPage(self.speech, self.phrases.speech.title)

        but_save = wx.Button(self, wx.ID_OK, parent.phrases.settings.save)
        but_cancel = wx.Button(self, wx.ID_CANCEL, parent.phrases.settings.cancel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_but = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        sizer_but.Add(but_save, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        sizer_but.Add(but_cancel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(notebook, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sizer_but, 0, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer)


class TabGeneral(wx.Panel):
    """Page notebook for general settings."""

    def __init__(self, parent, drawer, config, phrases):
        """Initialization page for general settings."""
        super().__init__(parent, wx.ID_ANY)
        self.drawer = drawer
        self.config = config

        self.names = []
        self.codes = []
        for code, name in self.config['languages'].items():
            self.names.append(name)
            self.codes.append(code)

        box_lang = wx.StaticBox(self, wx.ID_ANY, phrases.box_lang)
        self.languages = wx.Choice(box_lang, wx.ID_ANY, choices=self.names)
        self.expand = wx.CheckBox(self, wx.ID_ANY, phrases.expand)
        box_readonly = wx.StaticBox(self, wx.ID_ANY, phrases.box_readonly)
        self.password_chk = wx.CheckBox(box_readonly, wx.ID_ANY, phrases.password_chk)
        self.password_btn = wx.Button(box_readonly, wx.ID_ANY, phrases.password_btn)

        sizer = wx.BoxSizer(wx.VERTICAL)
        lang_sizer = wx.StaticBoxSizer(box_lang, wx.HORIZONTAL)
        lang_sizer.Add(self.languages, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(lang_sizer, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.expand, 0, wx.EXPAND | wx.ALL, 5)
        readonly_sizer = wx.StaticBoxSizer(box_readonly, wx.HORIZONTAL)
        readonly_sizer.Add(self.password_chk, 1, wx.EXPAND | wx.ALL, 5)
        readonly_sizer.Add(self.password_btn, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(readonly_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_CHOICE, getattr(self, 'choice_language'), self.languages)
        self.Bind(wx.EVT_CHECKBOX, getattr(self, 'change_expand'), self.expand)
        self.Bind(wx.EVT_CHECKBOX, getattr(self, 'change_password'), self.password_chk)
        self.Bind(wx.EVT_BUTTON, getattr(self, 'set_password'), self.password_btn)

        self.languages.SetSelection(self.codes.index(self.config['general_language']))
        expand = True if self.config["general_expand"] == "true" else False
        self.expand.SetValue(expand)
        password_chk = True if self.config["readonly_password_check"] == "true" else False
        self.password_chk.SetValue(password_chk)

    def choice_language(self, event):
        """Select language for interface."""
        self.config['general_language'] = self.codes[self.languages.GetSelection()]

    def change_expand(self, event):
        """Change expand value in checkbox."""
        expand = "true" if self.expand.GetValue() else "false"
        self.config['general_expand'] = expand

    def change_password(self, event):
        """Change password readonly value in checkbox."""
        password_chk = "true" if self.password_chk.GetValue() else "false"
        self.config['readonly_password_check'] = password_chk

    def set_password(self, event):
        """Change password readonly in config."""
        dlg = PasswordEntryDialog(self.drawer, self.drawer.phrases.titles.password)
        if RetCode.OK == dlg.ShowModal():
            hashpass= hashlib.sha1(dlg.GetValue().encode("utf-8"))
            self.config['readonly_password'] = hashpass.hexdigest()
        dlg.Destroy()


class TabState(wx.Panel):
    """Page notebook for state settings."""

    def __init__(self, parent, drawer, config, phrases):
        """Initialization page for state settings."""
        super().__init__(parent, wx.ID_ANY)
        self.config = config

        box_user_states = wx.StaticBox(self, wx.ID_ANY, phrases.box_user_states)
        self.user_states = wx.ListBox(box_user_states, wx.ID_ANY, choices=self.config['states'], style=wx.LB_SINGLE | wx.LB_HSCROLL)
        self.but_up = wx.Button(box_user_states, wx.ID_ANY, phrases.but_up)
        self.but_down = wx.Button(box_user_states, wx.ID_ANY, phrases.but_down)
        self.but_del = wx.Button(box_user_states, wx.ID_ANY, phrases.but_del)

        box_new_state = wx.StaticBox(self, wx.ID_ANY, phrases.box_new_state)
        self.new_state = wx.TextCtrl(box_new_state, wx.ID_ANY)
        self.but_add = wx.Button(box_new_state, wx.ID_ANY, phrases.but_add)

        sizer = wx.BoxSizer(wx.VERTICAL)
        first_sizer = wx.BoxSizer(wx.HORIZONTAL)
        user_states_sizer = wx.StaticBoxSizer(box_user_states, wx.VERTICAL)
        user_states_sizer.Add(self.user_states, 1, wx.EXPAND | wx.ALL, 5)
        but_user_states_sizer = wx.GridSizer(rows=1, cols=3, hgap=5, vgap=5)
        but_user_states_sizer.Add(self.but_up, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        but_user_states_sizer.Add(self.but_down, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        but_user_states_sizer.Add(self.but_del, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        user_states_sizer.Add(but_user_states_sizer, 0, wx.EXPAND | wx.ALL, 5)
        first_sizer.Add(user_states_sizer, 1, wx.EXPAND | wx.ALL)
        sizer.Add(first_sizer, 1, wx.EXPAND | wx.ALL)
        second_sizer = wx.StaticBoxSizer(box_new_state, wx.HORIZONTAL)
        second_sizer.Add(self.new_state, 1, wx.EXPAND | wx.ALL, 5)
        second_sizer.Add(self.but_add, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(second_sizer, 0, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_LISTBOX, self.select_user_state, self.user_states)
        self.Bind(wx.EVT_TEXT, self.edit_new_state, self.new_state)
        self.Bind(wx.EVT_BUTTON, self.add, self.but_add)
        self.Bind(wx.EVT_BUTTON, self.position, self.but_up)
        self.Bind(wx.EVT_BUTTON, self.position, self.but_down)
        self.Bind(wx.EVT_BUTTON, self.delete, self.but_del)

        self.but_up.Enable(False)
        self.but_down.Enable(False)
        self.but_del.Enable(False)
        self.but_add.Enable(False)

    def select_user_state(self, event):
        """Change selection state in listbox."""
        index = self.user_states.GetSelection()
        self.but_up.Enable(True)
        self.but_down.Enable(True)
        self.but_del.Enable(True)
        if index == 0:
            self.but_up.Enable(False)
        if index == self.user_states.GetCount()-1:
            self.but_down.Enable(False)

    def edit_new_state(self, event):
        """Edit new state field."""
        self.but_add.Enable(True)

    def position(self, event):
        """Press up or down buttons."""
        index = self.user_states.GetSelection()
        if event.GetId() == self.but_up.GetId():
            temp = self.user_states.GetString(index-1)
            self.user_states.SetString(index-1, self.user_states.GetString(index))
            self.user_states.SetString(index, temp)
        elif event.GetId() == self.but_down.GetId():
            temp = self.user_states.GetString(index+1)
            self.user_states.SetString(index+1, self.user_states.GetString(index))
            self.user_states.SetString(index, temp)
        self.config['states'] = [self.user_states.GetString(i) for i in range(self.user_states.GetCount())]

    def delete(self, event):
        """Delete state from user list states."""
        index = self.user_states.GetSelection()
        self.user_states.Delete(index)
        self.config['states'].pop(index)
        self.but_del.Enable(False)
        index = index-1 if index > 0 else 0
        self.user_states.SetSelection(index)

    def add(self, event):
        """Add new state in user states list."""
        state = self.new_state.GetValue()
        self.config['states'].append(state)
        self.user_states.Append(state)
        self.new_state.SetValue('')
        self.but_add.Enable(False)


class TabSpeech(wx.Panel):
    """Page notebook for speech settings."""

    def __init__(self, parent, drawer, config, phrases):
        """Initialization page for speech settings."""
        super().__init__(parent, wx.ID_ANY)
        self.config = config

        self.readonly = wx.CheckBox(self, wx.ID_ANY, phrases.readonly)
        self.state = wx.CheckBox(self, wx.ID_ANY, phrases.state)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.readonly, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.state, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_CHECKBOX, self.change_readonly, self.readonly)
        self.Bind(wx.EVT_CHECKBOX, self.change_state, self.state)

        readonly = True if self.config["speech_readonly"] == "true" else False
        self.readonly.SetValue(readonly)
        state = True if self.config["speech_state"] == "true" else False
        self.state.SetValue(state)

    def change_readonly(self, event):
        """Change readonly value in checkbox."""
        readonly = "true" if self.readonly.GetValue() else "false"
        self.config['speech_readonly'] = readonly

    def change_state(self, event):
        """Change state value in checkbox."""
        state = "true" if self.state.GetValue() else "false"
        self.config['speech_state'] = state
