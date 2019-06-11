"""
Graphical form for notes.

Created on 25.05.2019

@author: Ruslan Dolovanyuk

"""

from commands import Commands

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
        super().__init__(None, wx.ID_ANY, 'Заметки')
        self.command = Commands(self)

        self.panel = wx.Panel(self, wx.ID_ANY)
        sizer_panel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_panel.Add(self.panel, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer_panel)

        self.CreateStatusBar()
        self.__create_menu()
        self.__create_widgets()
        self.__create_bindings()

        self.command.init_tree()
        self.but_save.Disable()
        self.but_del.Disable()
        self.save_note.Enable(False)
        self.del_note.Enable(False)

    def __create_menu(self):
        """Create menu program."""
        menu_file = wx.Menu()
        self.create_root = menu_file.Append(-1, 'Создать ветку', 'Нажмите для создания записи в корне')
        self.create_child = menu_file.Append(-1, 'Создать запись', 'Нажмите для создания дочерней записи')
        self.save_note = menu_file.Append(-1, 'Сохранить запись', 'Нажмите для сохранения записи')
        self.del_note = menu_file.Append(-1, 'Удалить запись', 'Нажмите для удаления записи')
        menu_file.AppendSeparator()
        self.exit = menu_file.Append(-1, 'Выход', 'Нажмите для выхода из программы')

        menu_info = wx.Menu()
        self.count_root = menu_info.Append(-1, 'Количество веток', 'Нажмите для информации о количестве веток')
        self.count_child = menu_info.Append(-1, 'Количество записей', 'Нажмите для информации о количестве дочерних записей')
        self.count_total = menu_info.Append(-1, 'Количество всего', 'Нажмите для информации об общем количестве записей')

        menu_options = wx.Menu()
        self.options = menu_options.Append(-1, 'Настройки...', 'Нажмите для изменения настроек программы')

        menu_help = wx.Menu()
        self.about = menu_help.Append(-1, 'О программе...', 'Нажмите для просмотра информации о программе')

        menuBar = wx.MenuBar()
        menuBar.Append(menu_file, 'Файл')
        menuBar.Append(menu_info, 'Информация')
        menuBar.Append(menu_options, 'Опции')
        menuBar.Append(menu_help, 'Справка')
        self.SetMenuBar(menuBar)

    def __create_widgets(self):
        """Create widgets program."""
        self.tree = wx.TreeCtrl(self.panel, wx.ID_ANY,
                                style=wx.TR_DEFAULT_STYLE |
                                      wx.TR_SINGLE |
                                      wx.TR_LINES_AT_ROOT |
                                      wx.TR_HAS_BUTTONS)
        box_title = wx.StaticBox(self.panel, wx.ID_ANY, 'Заголовок')
        self.title = wx.TextCtrl(box_title, wx.ID_ANY)
        box_data = wx.StaticBox(self.panel, wx.ID_ANY, 'Текст')
        self.data = wx.TextCtrl(box_data, wx.ID_ANY, style=wx.TE_MULTILINE)
        self.but_save = wx.Button(self.panel, wx.ID_ANY, 'Сохранить')
        self.but_del = wx.Button(self.panel, wx.ID_ANY, 'Удалить')
        self.but_create = wx.Button(self.panel, wx.ID_ANY, 'Создать')

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
        """Create bindings for menu, widgets and other events."""
        self.Bind(wx.EVT_CLOSE, getattr(self.command, 'close_window'))
        self.Bind(wx.EVT_TREE_SEL_CHANGED, getattr(self.command, 'tree_select'), self.tree)
        self.Bind(wx.EVT_TEXT, getattr(self.command, 'text_change'), self.title)
        self.Bind(wx.EVT_TEXT, getattr(self.command, 'text_change'), self.data)
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'save'), self.but_save)
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'delete'), self.but_del)
        self.Bind(wx.EVT_BUTTON, getattr(self.command, 'create'), self.but_create)

        self.Bind(wx.EVT_MENU, getattr(self.command, 'create'), self.create_root)
        self.Bind(wx.EVT_MENU, getattr(self.command, 'create'), self.create_child)
        self.Bind(wx.EVT_MENU, getattr(self.command, 'save'), self.save_note)
        self.Bind(wx.EVT_MENU, getattr(self.command, 'delete'), self.del_note)
        self.Bind(wx.EVT_MENU, getattr(self.command, 'close'), self.exit)
        self.Bind(wx.EVT_MENU, getattr(self.command, 'count'), self.count_root)
        self.Bind(wx.EVT_MENU, getattr(self.command, 'count'), self.count_child)
        self.Bind(wx.EVT_MENU, getattr(self.command, 'count'), self.count_total)
        self.Bind(wx.EVT_MENU, getattr(self.command, 'options'), self.options)
        self.Bind(wx.EVT_MENU, getattr(self.command, 'about'), self.about)
