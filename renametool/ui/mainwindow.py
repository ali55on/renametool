#!/usr/bin/env python3
import sys
import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib

from tools.title import Title
from tools.utils.file import File
from ui.header import StackHeader
from ui.selectfiles import SelectFiles
from ui.preview import Preview
from ui.footer import Footer


path = os.path.dirname(os.path.abspath(__file__))


class RenameToolWindow(Gtk.Window):
    """Rename tool Window

    Main application window with all widgets.
    """
    def __init__(self, file_list: list = list, *args, **kwargs) -> None:
        """Class constructor

        Initializes RenameToolWindow widgets.

        :param file_list: Python 'list' of 'File' objects
        """
        Gtk.Window.__init__(
            self, window_position=Gtk.WindowPosition.CENTER,
            *args, **kwargs)
        # Icon
        icon_url = path.replace('ui', 'data{}rename-tool.svg'.format(os.sep))
        self.set_default_icon_from_file(icon_url)
        
        # Args
        self.file_list = list(File(x) for x in file_list)

        # Flags
        self.files_preview = False

        # Window title
        self.__set_title()

        # Main box
        self.main_box = Gtk.VBox()
        self.add(self.main_box)

        # Header
        self.header = StackHeader()
        self.main_box.pack_start(self.header, True, True, 0)

        self.separator_top = Gtk.Separator(
            orientation=Gtk.Orientation.HORIZONTAL, valign=Gtk.Align.END)
        self.main_box.pack_start(self.separator_top, True, True, 0)

        # Create Stack
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
        self.stack.set_transition_duration(300)

        # Preview
        self.preview = Preview(header=self.header, file_list=self.file_list)

        # Select
        self.select_area = SelectFiles(file_list=self.file_list)

        # Set stack
        # self.stack_switcher.get_stack().get_visible_child_name()
        if self.file_list:
            self.stack.add_titled(self.preview, 'preview', 'preview')
            self.stack.add_titled(self.select_area, 'select', 'select')
        else:
            self.stack.add_titled(self.select_area, 'select', 'select')
            self.stack.add_titled(self.preview, 'preview', 'preview')

        self.main_box.pack_start(self.stack, True, True, 0)

        # Footer
        self.separator_bottom = Gtk.Separator(
            orientation=Gtk.Orientation.HORIZONTAL, valign=Gtk.Align.START)
        self.main_box.pack_start(self.separator_bottom, True, True, 0)

        self.footer = Footer(
            preview=self.preview,
            header=self.header,
            file_list=self.file_list,
            transient_for=self)
        self.main_box.pack_start(self.footer, True, True, 0)

        # Focus
        self.activate_focus()
        self.set_focus(self.header.tab_rename.entry)

        # Default
        self.activate_default()
        self.set_default(self.footer.button_rename)

        self.__widget_sensitivity_daemon ()

    def __widget_sensitivity_daemon (self) -> None:
        # Starts widget sensitivity daemon
        if not self.files_preview:
            GLib.idle_add(self.__change_widgets_sensitivity)
        GLib.timeout_add(300, self.__widget_sensitivity_daemon)

    def __change_widgets_sensitivity(self) -> None:
        # Sets the sensitivity of the widgets according to the
        # filling of the file list
        if self.header.get_sensitive():
            self.header.set_sensitive(False)
            self.separator_top.set_visible(False)
            self.separator_bottom.set_visible(False)

        self.file_list = self.select_area.get_file_list()
        if self.file_list:
            self.files_preview = True
            self.stack.set_visible_child(self.preview)
            self.preview.set_file_list(self.file_list)
            self.footer.set_file_list(self.file_list)
            self.header.set_sensitive(True)
            self.separator_top.set_visible(True)
            self.separator_bottom.set_visible(True)
            self.__set_title()

    def __set_title(self) -> None:
        # Sets the title of the application window
        if self.file_list:
            title_obj = Title(self.file_list)
            self.set_title(title_obj.get_title())
        else:
            self.set_title('Rename Tool')
