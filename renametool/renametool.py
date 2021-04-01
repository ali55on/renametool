#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import ui.mainwindow as main_window
import tools.utils.file as file


def run_main_app(file_list) -> None:
    """"""
    win = main_window.RenameToolWindow(file_list=file_list)
    win.connect('destroy', Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == '__main__':
    del(sys.argv[0])
    if sys.argv:
        if len(sys.argv) == 1:
            # run_mini_app()
            pass

        else:
            file_list = list(file.File(x) for x in sys.argv)
            run_main_app(file_list=file_list)
    else:
        file_list = list()
        run_main_app(file_list=file_list)

exit(1)


    
