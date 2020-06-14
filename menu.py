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
        self.drawer.undo.Enable(False)
        self.drawer.redo.Enable(False)
        self.drawer.order_up.Enable(False)
        self.drawer.order_down.Enable(False)
        self.drawer.order_parent_up.Enable(False)
        self.drawer.order_parent_down.Enable(False)
        self.drawer.sort_titles.Enable(False)
        self.drawer.sort_childcount_up.Enable(False)
        self.drawer.sort_childcount_down.Enable(False)
        self.drawer.sort_state_up.Enable(False)
        self.drawer.sort_state_down.Enable(False)
        self.drawer.info_date.Enable(False)

    def __create_menu(self):
        """Create menu program."""
        menu_file = wx.Menu()
        self.drawer.create_root = menu_file.Append(-1, self.phrases.menu.file.items.create_root.name, self.phrases.menu.file.items.create_root.help)
        self.drawer.create_child = menu_file.Append(-1, self.phrases.menu.file.items.create_child.name, self.phrases.menu.file.items.create_child.help)
        self.drawer.insert = menu_file.Append(-1, self.phrases.menu.file.items.insert.name, self.phrases.menu.file.items.insert.help)
        menu_file.AppendSeparator()
        self.drawer.save_note = menu_file.Append(-1, self.phrases.menu.file.items.save_note.name, self.phrases.menu.file.items.save_note.help)
        self.drawer.del_note = menu_file.Append(-1, self.phrases.menu.file.items.del_note.name, self.phrases.menu.file.items.del_note.help)
        menu_file.AppendSeparator()
        self.drawer.exit = menu_file.Append(-1, self.phrases.menu.file.items.exit.name, self.phrases.menu.file.items.exit.help)

        menu_edit = wx.Menu()
        self.drawer.undo = menu_edit.Append(-1, self.phrases.menu.edit.items.undo.name, self.phrases.menu.edit.items.undo.help)
        self.drawer.redo = menu_edit.Append(-1, self.phrases.menu.edit.items.redo.name, self.phrases.menu.edit.items.redo.help)
        menu_edit.AppendSeparator()
        menu_order = wx.Menu()
        self.drawer.order_up = menu_order.Append(-1, self.phrases.menu.edit.items.order.items.up.name, self.phrases.menu.edit.items.order.items.up.help)
        self.drawer.order_down = menu_order.Append(-1, self.phrases.menu.edit.items.order.items.down.name, self.phrases.menu.edit.items.order.items.down.help)
        menu_order_parent = wx.Menu()
        self.drawer.order_parent_up = menu_order_parent.Append(-1, self.phrases.menu.edit.items.order.items.parent.items.up.name, self.phrases.menu.edit.items.order.items.parent.items.up.help)
        self.drawer.order_parent_down = menu_order_parent.Append(-1, self.phrases.menu.edit.items.order.items.parent.items.down.name, self.phrases.menu.edit.items.order.items.parent.items.down.help)
        menu_order.Append(-1, self.phrases.menu.edit.items.order.items.parent.title, menu_order_parent)
        menu_edit.Append(-1, self.phrases.menu.edit.items.order.title, menu_order)
        menu_sort = wx.Menu()
        self.drawer.sort_titles = menu_sort.Append(-1, self.phrases.menu.edit.items.sort.items.titles.name, self.phrases.menu.edit.items.sort.items.titles.help)
        menu_sort_child = wx.Menu()
        self.drawer.sort_childcount_up = menu_sort_child.Append(-1, self.phrases.menu.edit.items.sort.items.child.items.up.name, self.phrases.menu.edit.items.sort.items.child.items.up.help)
        self.drawer.sort_childcount_down = menu_sort_child.Append(-1, self.phrases.menu.edit.items.sort.items.child.items.down.name, self.phrases.menu.edit.items.sort.items.child.items.down.help)
        menu_sort.Append(-1, self.phrases.menu.edit.items.sort.items.child.title, menu_sort_child)
        menu_sort_state = wx.Menu()
        self.drawer.sort_state_up = menu_sort_state.Append(-1, self.phrases.menu.edit.items.sort.items.state.items.up.name, self.phrases.menu.edit.items.sort.items.state.items.up.help)
        self.drawer.sort_state_down = menu_sort_state.Append(-1, self.phrases.menu.edit.items.sort.items.state.items.down.name, self.phrases.menu.edit.items.sort.items.state.items.down.help)
        menu_sort.Append(-1, self.phrases.menu.edit.items.sort.items.state.title, menu_sort_state)
        menu_edit.Append(-1, self.phrases.menu.edit.items.sort.title, menu_sort)

        menu_info = wx.Menu()
        self.drawer.count_root = menu_info.Append(-1, self.phrases.menu.info.items.count_root.name, self.phrases.menu.info.items.count_root.help)
        self.drawer.count_child = menu_info.Append(-1, self.phrases.menu.info.items.count_child.name, self.phrases.menu.info.items.count_child.help)
        self.drawer.count_total = menu_info.Append(-1, self.phrases.menu.info.items.count_total.name, self.phrases.menu.info.items.count_total.help)
        menu_info.AppendSeparator()
        self.drawer.info_date = menu_info.Append(-1, self.phrases.menu.info.items.date.name, self.phrases.menu.info.items.date.help)

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
                                       (wx.ACCEL_CTRL, ord('Z'), self.drawer.undo.GetId()),
                                       (wx.ACCEL_CTRL, ord('Y'), self.drawer.redo.GetId()),
                                       (wx.ACCEL_CTRL, wx.WXK_UP, self.drawer.order_up.GetId()),
                                       (wx.ACCEL_CTRL, wx.WXK_DOWN, self.drawer.order_down.GetId()),
                                       (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, wx.WXK_UP, self.drawer.order_parent_up.GetId()),
                                       (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, wx.WXK_DOWN, self.drawer.order_parent_down.GetId()),
                                       (wx.ACCEL_CTRL, ord('I'), self.drawer.count_total.GetId()),
                                       (wx.ACCEL_CTRL, ord('O'), self.drawer.options.GetId()),
                                       ])
        self.drawer.SetAcceleratorTable(acceltbl)

    def __create_bindings(self):
        """Create bindings for menu."""
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'create'), self.drawer.create_root)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'create'), self.drawer.create_child)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'insert'), self.drawer.insert)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'save'), self.drawer.save_note)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'delete'), self.drawer.del_note)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'close'), self.drawer.exit)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'rollback'), self.drawer.undo)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'rollback'), self.drawer.redo)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'order'), self.drawer.order_up)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'order'), self.drawer.order_down)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'order'), self.drawer.order_parent_up)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'order'), self.drawer.order_parent_down)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'sort'), self.drawer.sort_titles)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'sort'), self.drawer.sort_childcount_up)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'sort'), self.drawer.sort_childcount_down)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'sort'), self.drawer.sort_state_up)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'sort'), self.drawer.sort_state_down)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'count'), self.drawer.count_root)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'count'), self.drawer.count_child)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'count'), self.drawer.count_total)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'info_date'), self.drawer.info_date)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'options'), self.drawer.options)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'donate'), self.drawer.donate)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'home'), self.drawer.home)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'about'), self.drawer.about)
