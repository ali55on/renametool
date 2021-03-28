#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import ui.gtkmain as gtk_main
import tools.utils.file as file


del(sys.argv[0])
list_files = list(file.File(x) for x in sys.argv)


if __name__ == '__main__':
    win = gtk_main.MyWindow(list_files)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
