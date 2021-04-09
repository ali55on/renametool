#!/usr/bin/env python3
import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

from tools.settings import UserSettings


settings = UserSettings()
path = os.path.dirname(os.path.abspath(__file__))


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
            self, modal=True,
            type_hint=1, title='Preferences',
            resizable=False, *args, **kwargs)
        # Icon
        icon_url = path.replace('ui', 'data{}rename-tool.svg'.format(os.sep))
        self.set_default_icon_from_file(icon_url)

        # Main container
        self.main_box = Gtk.VBox()
        self.add(self.main_box)
