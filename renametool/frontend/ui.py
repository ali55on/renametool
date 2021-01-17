#!/usr/bin/env python3
import os
import sys

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import frontend.gtk.main as gtk_main
import backend.utils.file as file


del(sys.argv[0])
list_files = list(file.File(x) for x in sys.argv)


class GtkUi(object):
    def __init__(self):
        self.list_files = list_files

    def main(self):
        win = gtk_main.MyWindow(self.list_files)
        win.connect("destroy", Gtk.main_quit)
        win.show_all()
        Gtk.main()


class ChangeUi(object):
    def __init__(self):
        self.gtk_ui = GtkUi()

    def main(self):
        self.gtk_ui.main()
