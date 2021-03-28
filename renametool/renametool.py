#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import ui.mainwindow as main_window
import ui.emptystartwindow as empty_start_window
import tools.utils.file as file


del(sys.argv[0])
if sys.argv:
    list_files = list(file.File(x) for x in sys.argv)
else:
    files = empty_start_window.EmptyWindow().get_file_list()
    print(files)
    if files:
        list_files = list(file.File(x) for x in files)
    else:
        exit(1)


if __name__ == '__main__':
    win = main_window.RenameToolWindow(list_files)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
