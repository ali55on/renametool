#!/usr/bin/env python3
import sys
import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import tools.title as title
import tools.utils.file as file
import tools.settings as settings
import ui.header as header
import ui.preview as preview
import ui.base as base


class MyWindow(Gtk.Window):
    def __init__(self, list_files: list = list):
        Gtk.Window.__init__(
            self, window_position=Gtk.WindowPosition.CENTER,
            icon_name='document-edit-symbolic')
        # Args
        self.list_files = list_files

        # Settings
        self.settings = settings.UserSettings()
        self.markup_settings = self.settings.get_markup_settings()
        self.color_settings = self.settings.get_color_settings()

        # Flags
        self.status_error = None

        # Window title
        title_obj = title.Title(self.list_files)
        self.set_title(title_obj.get_title())

        # Main box
        self.main_box = Gtk.VBox()
        self.add(self.main_box)

        # Header
        self.header = header.StackHeader(markup_settings=self.markup_settings)
        self.main_box.pack_start(self.header, True, True, 0)

        # Preview
        sep_up = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, valign=Gtk.Align.END)
        self.main_box.pack_start(sep_up, True, True, 0)

        self.preview = preview.Preview(
            header=self.header, color_settings=self.color_settings, markup_settings=self.markup_settings,
            list_files=self.list_files)
        self.main_box.pack_start(self.preview, True, True, 0)

        # Base
        sep_dw = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, valign=Gtk.Align.START)
        self.main_box.pack_start(sep_dw, True, True, 0)

        self.base = base.Base(
            preview=self.preview, color_settings=self.color_settings, list_files=self.list_files,
            transient=self)
        self.main_box.pack_start(self.base, True, True, 0)

        # Focus
        self.activate_focus()
        self.set_focus(self.header.tab_rename.entry)

        # Default
        self.activate_default()
        self.set_default(self.base.button_rename)


if __name__ == '__main__':
    del (sys.argv[0])
    ls = os.listdir(os.path.dirname(os.path.abspath(__file__)))
    l_files = list(file.File(x) for x in sys.argv)

    win = MyWindow(l_files)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
