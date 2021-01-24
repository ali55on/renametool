#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class PreferencesWindow(Gtk.Window):
    def __init__(self, *args, **kwargs):
        Gtk.Window.__init__(
            self, icon_name='preferences-system-symbolic',
            type_hint=1, title='Rename Tool - Preferences', *args, **kwargs)
        self.main_box = PreferencesBox()
        self.add(self.main_box)


class PreferencesBox(Gtk.VBox):
    def __init__(self, *args, **kwargs):
        """"""
        Gtk.VBox.__init__(self, margin=18, *args, **kwargs)
        self.pack_start(Gtk.Label(label='Preferences'), True, True, 0)
