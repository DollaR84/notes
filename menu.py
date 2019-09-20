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
        self.command = self.drawer.command

        self.__create_menu()
        self.__create_accel()
        self.__create_bindings()

        self.drawer.save_note.Enable(False)
        self.drawer.del_note.Enable(False)

    def __create_menu(self):
        """Create menu program."""
        menu_file = wx.Menu()
        self.drawer.create_root = menu_file.Append(-1, 'Создать ветку', 'Нажмите для создания записи в корне')
        self.drawer.create_child = menu_file.Append(-1, 'Создать запись', 'Нажмите для создания дочерней записи')
        self.drawer.save_note = menu_file.Append(-1, 'Сохранить запись', 'Нажмите для сохранения записи')
        self.drawer.del_note = menu_file.Append(-1, 'Удалить запись', 'Нажмите для удаления записи')
        menu_file.AppendSeparator()
        self.drawer.exit = menu_file.Append(-1, 'Выход', 'Нажмите для выхода из программы')

        menu_info = wx.Menu()
        self.drawer.count_root = menu_info.Append(-1, 'Количество веток', 'Нажмите для информации о количестве веток')
        self.drawer.count_child = menu_info.Append(-1, 'Количество записей', 'Нажмите для информации о количестве дочерних записей')
        self.drawer.count_total = menu_info.Append(-1, 'Количество всего', 'Нажмите для информации об общем количестве записей')

        menu_options = wx.Menu()
        self.drawer.options = menu_options.Append(-1, 'Настройки...', 'Нажмите для изменения настроек программы')

        menu_help = wx.Menu()
        self.drawer.donate = menu_help.Append(-1, 'Донат...', 'Нажмите для поддержания дальнейшего развития проекта')
        self.drawer.about = menu_help.Append(-1, 'О программе...', 'Нажмите для просмотра информации о программе')

        menuBar = wx.MenuBar()
        menuBar.Append(menu_file, 'Файл')
        menuBar.Append(menu_info, 'Информация')
        menuBar.Append(menu_options, 'Опции')
        menuBar.Append(menu_help, 'Справка')
        self.drawer.SetMenuBar(menuBar)

    def __create_accel(self):
        """Create accelerated table for menu."""
        acceltbl = wx.AcceleratorTable([
                                       (wx.ACCEL_CTRL, ord('N'), self.drawer.create_child.GetId()),
                                       (wx.ACCEL_CTRL, ord('S'), self.drawer.save_note.GetId()),
                                       (wx.ACCEL_CTRL, ord('Q'), self.drawer.exit.GetId()),
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
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'count'), self.drawer.count_root)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'count'), self.drawer.count_child)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'count'), self.drawer.count_total)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'options'), self.drawer.options)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'donate'), self.drawer.donate)
        self.drawer.Bind(wx.EVT_MENU, getattr(self.command, 'about'), self.drawer.about)
