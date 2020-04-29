"""
Menu module for project.

Created on 20.09.2019

@author: Ruslan Dolovanyuk

"""

import wx


class Menu:
    """Create menu for project."""

    def __init__(self, parent):
        """Initialization menu."""
        self.drawer = parent
        self.phrases = self.drawer.phrases
        self.command = self.drawer.command

        self.__create_menu()
        self.__create_accel()
        self.__create_bindings()

        self.drawer.save_note.Enable(False)
        self.drawer.del_note.Enable(False)
        self.drawer.order_up.Enable(False)
        self.drawer.order_down.Enable(False)
        self.drawer.sort_name.Enable(False)
        self.drawer.sort_childcount.Enable(False)

    def __create_menu(self):
        """Create menu program."""
        menu_file = wx.Menu()
        self.drawer.create_root = menu_file.Append(-1, self.phrases.menu.file.items.create_root.name, self.phrases.menu.file.items.create_root.help)
        self.drawer.create_child = menu_file.Append(-1, self.phrases.menu.file.items.create_child.name, self.phrases.menu.file.items.create_child.help)
        self.drawer.save_note = menu_file.Append(-1, self.phrases.menu.file.items.save_note.name, self.phrases.menu.file.items.save_note.help)
        self.drawer.del_note = menu_file.Append(-1, self.phrases.menu.file.items.del_note.name, self.phrases.menu.file.items.del_note.help)
        menu_file.AppendSeparator()
        self.drawer.exit = menu_file.Append(-1, self.phrases.menu.file.items.exit.name, self.phrases.menu.file.items.exit.help)

        menu_edit = wx.Menu()
        menu_order = wx.Menu()
        self.drawer.order_up = menu_order.Append(-1, self.phrases.menu.edit.items.order.items.up.name, self.phrases.menu.edit.items.order.items.up.help)
        self.drawer.order_down = menu_order.Append(-1, self.phrases.menu.edit.items.order.items.down.name, self.phrases.menu.edit.items.order.items.down.help)
        menu_edit.Append(-1, self.phrases.menu.edit.items.order.title, menu_order)
        menu_sort = wx.Menu()
        self.drawer.sort_titles = menu_sort.Append(-1, self.phrases.menu.edit.items.sort.items.titles.name, self.phrases.menu.edit.items.sort.items.titles.help)
        self.drawer.sort_childcount = menu_sort.Append(-1, self.phrases.menu.edit.items.sort.items.child.name, self.phrases.menu.edit.items.sort.items.child.help)
        menu_edit.Append(-1, self.phrases.menu.edit.items.sort.title, menu_sort)

        menu_info = wx.Menu()
        self.drawer.count_root = menu_info.Append(-1, self.phrases.menu.info.items.count_root.name, self.phrases.menu.info.items.count_root.help)
        self.drawer.count_child = menu_info.Append(-1, self.phrases.menu.info.items.count_child.name, self.phrases.menu.info.items.count_child.help)
        self.drawer.count_total = menu_info.Append(-1, self.phrases.menu.info.items.count_total.name, self.phrases.menu.info.items.count_total.help)

        menu_options = wx.Menu()
        self.drawer.options = menu_options.Append(-1, self.phrases.menu.options.items.settings.name, self.phrases.menu.options.items.settings.help)

        menu_help = wx.Menu()
        self.drawer.donate = menu_help.Append(-1, self.phrases.menu.help.items.donate.name, self.phrases.menu.help.items.donate.help)
        self.drawer.home = menu_help.Append(-1, self.phrases.menu.help.items.home.name, self.phrases.menu.help.items.home.help)
        self.drawer.about = menu_help.Append(-1, self.phrases.menu.help.items.about.name, self.phrases.menu.help.items.about.help)

        menuBar = wx.MenuBar()
        menuBar.Append(menu_file, self.phrases.menu.file.title)
        menuBar.Append(menu_edit, self.phrases.menu.edit.title)
        menuBar.Append(menu_info, self.phrases.menu.info.title)
        menuBar.Append(menu_options, self.phrases.menu.options.title)
        menuBar.Append(menu_help, self.phrases.menu.help.title)
        self.drawer.SetMenuBar(menuBar)

    def __create_accel(self):
        """Create accelerated table for menu."""
        acceltbl = wx.AcceleratorTable([
                                       (wx.ACCEL_CTRL, ord('N'), self.drawer.create_child.GetId()),
                                       (wx.ACCEL_CTRL, ord('S'), self.drawer.save_note.GetId()),
                                       (wx.ACCEL_CTRL, ord('Q'), self.drawer.exit.GetId()),
                                       (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, wx.WXK_UP, self.drawer.order_up.GetId()),
                                       (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, wx.WXK_DOWN, self.drawer.order_down.GetId()),
                                       (wx.ACCEL_CTRL, ord('I'), self.drawer.count_total.GetId()),
                                       (wx.ACCEL_CTRL, ord('O'), self.drawer.options.GetId()),
                                       ])
        self.drawer.SetAcceleratorTable(acceltbl)

    def __create_bindings(self):
        """Create bindings for menu."""
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'create'), self.drawer.create_root)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'create'), self.drawer.create_child)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'save'), self.drawer.save_note)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'delete'), self.drawer.del_note)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'close'), self.drawer.exit)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'order'), self.drawer.order_up)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'order'), self.drawer.order_down)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'sort'), self.drawer.sort_titles)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'sort'), self.drawer.sort_childcount)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'count'), self.drawer.count_root)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'count'), self.drawer.count_child)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'count'), self.drawer.count_total)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'options'), self.drawer.options)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'donate'), self.drawer.donate)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'home'), self.drawer.home)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'about'), self.drawer.about)
