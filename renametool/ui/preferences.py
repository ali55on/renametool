#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

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
            type_hint=1, title='Rename Tool - Preferences', *args, **kwargs)

        # Main container
        self.notebook = Gtk.Notebook(show_border=False)
        self.add(self.notebook)

        self.app_page = AppPage()
        self.notebook.append_page(self.app_page, Gtk.Label(label="App"))

        self.markup_page = MarkupPage()
        self.notebook.append_page(
            self.markup_page, Gtk.Label(label="Templates"))

        self.color_page = ColorPage()
        self.notebook.append_page(
            self.color_page, Gtk.Label(label="Colors"))


class AppPage(Gtk.VBox):
    """App Page box"""
    def __init__(self, *args, **kwargs) -> None:
        """Class constructor

        Initializes App Page widgets.

        :param app_settings: A 'dictionary' with app settings
        """
        Gtk.Box.__init__(self, margin=18, *args, **kwargs)
        self.pack_start(Gtk.Label(label='App Preferences'), True, True, 0)


class MarkupPage(Gtk.VBox):
    """Markup Page box"""
    def __init__(self, *args, **kwargs) -> None:
        """Class constructor

        Initializes Markup Page widgets.

        :param markup_settings: A 'dictionary' with markup settings
        """
        Gtk.Box.__init__(self, margin=18, *args, **kwargs)

        # Settings
        self.markup_settings = settings.get_markup_settings()
        self.pack_start(Gtk.Label(label='Template Preferences'), True, True, 0)


class ColorPage(Gtk.VBox):
    """Color Page box"""
    def __init__(self, *args, **kwargs) -> None:
        """Class constructor

        Initializes Color Page widgets.

        :param color_settings: A 'dictionary' with color settings
        """
        Gtk.Box.__init__(self, margin=18, *args, **kwargs)

        # Settings
        self.color_settings = settings.get_color_settings()
        self.pack_start(Gtk.Label(label='Color Preferences'), True, True, 0)


