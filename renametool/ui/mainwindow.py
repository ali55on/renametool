#!/usr/bin/env python3
import sys
import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib

import tools.title as title
import tools.utils.file as file
import tools.settings as settings
import ui.header as header
import ui.selectfiles as select_files
import ui.preview as preview
import ui.base as base


class RenameToolWindow(Gtk.Window):
    def __init__(self, file_list: list = list, *args, **kwargs):
        Gtk.Window.__init__(
            self, window_position=Gtk.WindowPosition.CENTER,
            icon_name='document-edit-symbolic', *args, **kwargs)
        
        # Args
        self.file_list = file_list

        # Settings
        self.settings = settings.UserSettings()
        self.markup_settings = self.settings.get_markup_settings()
        self.color_settings = self.settings.get_color_settings()

        # Flags
        self.status_error = None
        self.files_preview = False

        # Window title
        if self.file_list:
            title_obj = title.Title(self.file_list)
            self.set_title(title_obj.get_title())
        else:
            self.set_title('Rename Tool')

        # Main box
        self.main_box = Gtk.VBox()
        self.add(self.main_box)

        # Header
        self.header = header.StackHeader(markup_settings=self.markup_settings)
        self.main_box.pack_start(self.header, True, True, 0)

        sep_up = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, valign=Gtk.Align.END)
        self.main_box.pack_start(sep_up, True, True, 0)

        # Create Stack
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
        self.stack.set_transition_duration(300)

        # Preview
        self.preview = preview.Preview(
            header=self.header, color_settings=self.color_settings,
            markup_settings=self.markup_settings,
            file_list=self.file_list)

        # Select
        self.select_area = select_files.SelectFiles(file_list=self.file_list)

        # Set stack
        # self.active_work_tab = self.stack_switcher.get_stack().get_visible_child_name()
        if self.file_list:
            self.stack.add_titled(self.preview, 'preview', 'preview')
            self.stack.add_titled(self.select_area, 'select', 'select')
        else:
            self.stack.add_titled(self.select_area, 'select', 'select')
            self.stack.add_titled(self.preview, 'preview', 'preview')

        self.main_box.pack_start(self.stack, True, True, 0)

        # Base
        sep_dw = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL, valign=Gtk.Align.START)
        self.main_box.pack_start(sep_dw, True, True, 0)

        self.base = base.Base(
            preview=self.preview, color_settings=self.color_settings, file_list=self.file_list,
            transient=self)
        self.main_box.pack_start(self.base, True, True, 0)

        # Focus
        self.activate_focus()
        self.set_focus(self.header.tab_rename.entry)

        # Default
        self.activate_default()
        self.set_default(self.base.button_rename)

        self.preview_daemon()

    def preview_daemon(self):
        if not self.files_preview:
            GLib.idle_add(self.preview_daemon_glib)
        GLib.timeout_add(300, self.preview_daemon)

    def preview_daemon_glib(self):
        self.file_list = self.select_area.get_file_list()
        if self.file_list:
            self.files_preview = True
            self.stack.set_visible_child(self.preview)
            self.preview.set_file_list(self.file_list)
            self.base.set_file_list(self.file_list)


if __name__ == '__main__':
    del (sys.argv[0])
    ls = os.listdir(os.path.dirname(os.path.abspath(__file__)))
    l_files = list(file.File(x) for x in sys.argv)

    win = RenameToolWindow(l_files)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
