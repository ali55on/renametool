#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class PreferencesWindow(Gtk.Window):
    """Preferences Window

    RenameTool application preferences window.
    """
    def __init__(
            self, 
            markup_settings: dict, color_settings: dict,
            *args, **kwargs) -> None:
        """Class constructor

        Initializes Preferences Window widgets.

        :param markup_settings: A 'dictionary' with markup settings
        """
        Gtk.Window.__init__(
            self, icon_name='preferences-system-symbolic', modal=True,
            type_hint=1, title='Rename Tool - Preferences', *args, **kwargs)

        # Args
        self.markup_settings = markup_settings
        self.color_settings = color_settings

        # Main container
        self.notebook = Gtk.Notebook(show_border=False)
        self.add(self.notebook)

        self.app_page = AppPage()  # app_settings=self.app_settings
        self.notebook.append_page(self.app_page, Gtk.Label(label="App"))

        self.markup_page = MarkupPage(markup_settings=self.markup_settings)
        self.notebook.append_page(
            self.markup_page, Gtk.Label(label="Templates"))

        self.color_page = ColorPage(color_settings=self.color_settings)
        self.notebook.append_page(
            self.color_page, Gtk.Label(label="Colors"))


class AppPage(Gtk.VBox):
    """App Page box"""
    def __init__(self, app_settings: dict = None, *args, **kwargs) -> None:
        """Class constructor

        Initializes App Page widgets.

        :param app_settings: A 'dictionary' with app settings
        """
        Gtk.Box.__init__(self, margin=18, *args, **kwargs)

        # Args
        self.app_settings = app_settings

        self.pack_start(Gtk.Label(label='App Preferences'), True, True, 0)


class MarkupPage(Gtk.VBox):
    """Markup Page box"""
    def __init__(self, markup_settings: dict = None, *args, **kwargs) -> None:
        """Class constructor

        Initializes Markup Page widgets.

        :param markup_settings: A 'dictionary' with markup settings
        """
        Gtk.Box.__init__(self, margin=18, *args, **kwargs)

        # Args
        self.markup_settings = markup_settings

        self.pack_start(Gtk.Label(label='Template Preferences'), True, True, 0)


class ColorPage(Gtk.VBox):
    """Color Page box"""
    def __init__(self, color_settings: dict = None, *args, **kwargs) -> None:
        """Class constructor

        Initializes Color Page widgets.

        :param color_settings: A 'dictionary' with color settings
        """
        Gtk.Box.__init__(self, margin=18, *args, **kwargs)

        # Args
        self.color_settings = color_settings
        print(self.color_settings)

        self.pack_start(Gtk.Label(label='Color Preferences'), True, True, 0)


