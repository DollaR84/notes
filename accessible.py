"""
Accessible classes for extend information of screen readers.

Created on 02.06.2020

@author: Ruslan Dolovanyuk

"""

import wx


class TreeAccessible(wx.Accessible):
    """Extend information for tree items."""

    def __init__(self, window):
        """Initialize accessible for treectrl."""
        self.window = window
        self.config = self.window.config
        super().__init__(window)

    def GetDescription(self, index):
        """Return extend text information for screen readers."""
        text = ''
        state = True if self.config.speech_state == "true" else False
        if state and self.window.state_check.IsEnabled() and self.window.state_check.IsChecked():
            text = '; '.join([text, self.window.states.GetString(self.window.states.GetSelection())])
        readonly = True if self.config.speech_readonly == "true" else False
        if readonly and self.window.readonly.IsEnabled() and self.window.readonly.IsChecked():
            text = '; '.join([text, self.window.readonly.GetLabel()])
        return (wx.ACC_OK, text)
