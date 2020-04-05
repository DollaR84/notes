"""
Graphic form change settings.

Created on 29.05.2019

@author: Ruslan Dolovanyuk

"""

import wx


class SettingsDialog(wx.Dialog):
    """Create interface settings dialog."""

    def __init__(self, parent, config):
        """Initialize interface."""
        super().__init__(parent, wx.ID_ANY, parent.phrases.settings.title)
        self.phrases = parent.phrases.settings
        self.config = {key: getattr(config, key) for key in config.ids.keys()}
        self.config['languages'] = config.get_languages()

        notebook = wx.Notebook(self, wx.ID_ANY)
        self.general = TabGeneral(notebook, self.config, self.phrases.general)
        notebook.AddPage(self.general, self.phrases.general.title)

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

    def __init__(self, parent, config, phrases):
        """Initialization page for general settings."""
        super().__init__(parent, wx.ID_ANY)
        self.config = config

        self.names = []
        self.codes = []
        for code, name in self.config['languages'].items():
            self.names.append(name)
            self.codes.append(code)

        box_lang = wx.StaticBox(self, wx.ID_ANY, phrases.box_lang)
        self.languages = wx.Choice(box_lang, wx.ID_ANY, choices=self.names)
        self.expand = wx.CheckBox(self, wx.ID_ANY, phrases.expand)

        sizer = wx.BoxSizer(wx.VERTICAL)
        lang_sizer = wx.StaticBoxSizer(box_lang, wx.HORIZONTAL)
        lang_sizer.Add(self.languages, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(lang_sizer, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.expand, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_CHOICE, getattr(self, 'choice_language'), self.languages)
        self.Bind(wx.EVT_CHECKBOX, getattr(self, 'change_expand'), self.expand)

        self.languages.SetSelection(self.codes.index(self.config['general_language']))
        expand = True if self.config["general_expand"] == "true" else False
        self.expand.SetValue(expand)

    def choice_language(self, event):
        """Select language for interface."""
        self.config['general_language'] = self.codes[self.languages.GetSelection()]

    def change_expand(self, event):
        """Change expand value in checkbox."""
        expand = "true" if self.expand.GetValue() else "false"
        self.config['general_expand'] = expand
