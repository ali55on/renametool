#!/usr/bin/env python3
import os
import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from ui.mainwindow import RenameToolWindow


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    """Run main Gtk app

    Run the application
    """
    del(sys.argv[0])
    win = RenameToolWindow(file_list=sys.argv)
    win.connect('destroy', Gtk.main_quit)
    win.show_all()
    Gtk.main()

    exit(1)


if __name__ == '__main__':
    main()

