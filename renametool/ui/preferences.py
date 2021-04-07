#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

from tools.settings import UserSettings


settings = UserSettings()


class PreferencesWindow(Gtk.Window):
    """Preferences Window

    RenameTool application preferences window.
    """
    def __init__(self, *args, **kwargs) -> None:
        """Class constructor

        Initializes Preferences Window widgets.

        :param markup_settings: A 'dictionary' with markup settings
        """
        Gtk.Window.__init__(
            self, icon_name='preferences-system-symbolic', modal=True,
            type_hint=1, title='Rename Tool - Preferences',
            resizable=False, *args, **kwargs)

        # Main container
        self.main_box = Gtk.VBox()
        self.add(self.main_box)
