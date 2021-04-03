#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from ui.mainwindow import RenameToolWindow
from tools.utils.file import File


def run_main_app(file_list: list) -> None:
    """Run main Gtk app

    Calls the application designed to work with more than one file name
    at the same time.
    Need a list of objects of type "File".
    """
    win = RenameToolWindow(file_list=file_list)
    win.connect('destroy', Gtk.main_quit)
    win.show_all()
    Gtk.main()


def run_mini_app(file: File) -> None:
    """Run mini app

    Calls the application designed to work with only one file name.
    Need a object of type "File".
    """
    print(type(file))


def main() -> None:
    """Main function

    The main function will define which app to call and which argument
    to pass.
    """
    del(sys.argv[0])
    if sys.argv:
        if len(sys.argv) == 1:
            file = File(sys.argv[0])
            run_mini_app(file=file)

        else:
            file_list = list(File(x) for x in sys.argv)
            run_main_app(file_list=file_list)
    else:
        file_list = list()
        run_main_app(file_list=file_list)

    exit(1)


if __name__ == '__main__':
    main()
