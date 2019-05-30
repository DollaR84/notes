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
        super().__init__(parent, wx.ID_ANY, 'Настройки')
        self.config = {key: getattr(config, key) for key in config.ids.keys()}

        but_save = wx.Button(self, wx.ID_OK, 'Сохранить')
        but_cancel = wx.Button(self, wx.ID_CANCEL, 'Отмена')

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_but = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        sizer_but.Add(but_save, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        sizer_but.Add(but_cancel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(sizer_but, 0, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer)

    def get_all(self):
        """Get all settings from controls."""
        pass
