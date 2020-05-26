"""
Collection template dialogs.

Created on 22.06.2017

@author: Ruslan Dolovanyuk

"""

import wx


class TextEntryDialog(wx.Dialog):
    """Class for input text from user."""

    def __init__(self, parent, caption, message='', default_value=''):
        """Initialize text entry dialog."""
        super().__init__(parent, wx.ID_ANY, caption)
        self.message = wx.StaticText(self, wx.ID_ANY, message,
                                     style=wx.ALIGN_LEFT)
        self.text = wx.TextCtrl(self, wx.ID_ANY, default_value)
        but_ok = wx.Button(self, wx.ID_OK, parent.phrases.dialogs.ok)
        but_cancel = wx.Button(self, wx.ID_CANCEL, parent.phrases.dialogs.cancel)

        sizer_but = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        sizer_but.Add(but_ok, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        sizer_but.Add(but_cancel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.message, 0, wx.ALIGN_LEFT, 5)
        sizer.Add(self.text, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sizer_but, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)
        self.Fit()

    def GetValue(self):
        """Return text entry in ctrl."""
        return self.text.GetValue()


class PasswordEntryDialog(wx.Dialog):
    """Class for input password from user."""

    def __init__(self, parent, caption, message='', default_value=''):
        """Initialize password entry dialog."""
        super().__init__(parent, wx.ID_ANY, caption)
        self.message = wx.StaticText(self, wx.ID_ANY, message,
                                     style=wx.ALIGN_LEFT)
        self.password = wx.TextCtrl(self, wx.ID_ANY, default_value, style=wx.TE_PASSWORD)
        but_ok = wx.Button(self, wx.ID_OK, parent.phrases.dialogs.ok)
        but_cancel = wx.Button(self, wx.ID_CANCEL, parent.phrases.dialogs.cancel)

        sizer_but = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        sizer_but.Add(but_ok, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        sizer_but.Add(but_cancel, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.message, 0, wx.ALIGN_LEFT, 5)
        sizer.Add(self.password, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sizer_but, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)
        self.Fit()

    def GetValue(self):
        """Return text entry in ctrl."""
        return self.password.GetValue()


class About(wx.Dialog):
    """Class about dialog."""

    def __init__(self, parent, caption, name, version, author):
        """Initialize dialog about form."""
        super().__init__(parent, wx.ID_ANY, caption)
        self.name = wx.StaticText(self, wx.ID_ANY, '"{}"'.format(name), style=wx.ALIGN_LEFT)
        self.version = wx.StaticText(self, wx.ID_ANY, '{}: {}'.format(parent.phrases.dialogs.version, version), style=wx.ALIGN_LEFT)
        self.author = wx.StaticText(self, wx.ID_ANY, '{}: {}'.format(parent.phrases.dialogs.author, author), style=wx.ALIGN_LEFT)
        close = wx.Button(self, wx.ID_OK, parent.phrases.dialogs.close)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.name, 0, wx.ALIGN_LEFT, 5)
        sizer.Add(self.version, 0, wx.ALIGN_LEFT, 5)
        sizer.Add(self.author, 0, wx.ALIGN_LEFT, 5)
        sizer.Add(close, 0, wx.ALIGN_CENTER, 5)
        self.SetSizer(sizer)
        self.Fit()


class Message:
    """Set functions for show standart MessageBoxes."""

    def __init__(self, parent):
        """Initialize message class."""
        self.parent = parent

    def information(self, title, message):
        """Show information MessageBox."""
        dlg = wx.MessageDialog(self.parent, message, title,
                               style=wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def error(self, title, message):
        """Show error MessageBox."""
        dlg = wx.MessageDialog(self.parent, message, title,
                               style=wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()

    def exclamation(self, title, message):
        """Show exclamation MessageBox."""
        dlg = wx.MessageDialog(self.parent, message, title,
                               style=wx.OK | wx.ICON_EXCLAMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def question(self, title, message):
        """Show question MessageBox."""
        ret_code = False
        dlg = wx.MessageDialog(self.parent, message, title,
                               style=wx.YES_NO | wx.NO_DEFAULT |
                               wx.ICON_QUESTION)
        dlg.SetYesNoLabels(self.parent.phrases.dialogs.yes, self.parent.phrases.dialogs.no)
        if wx.ID_YES == dlg.ShowModal():
            ret_code = True
        dlg.Destroy()
        return ret_code


class RetCode:
    """Content return code wxpython."""

    OK = wx.ID_OK
    CANCEL = wx.ID_CANCEL
