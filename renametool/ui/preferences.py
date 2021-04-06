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
        self.notebook.append_page(self.app_page, Gtk.Label(label="Application"))

        self.markup_page = MarkupPage()
        self.notebook.append_page(
            self.markup_page, Gtk.Label(label="Rename tools"))

        self.color_page = ColorPage()
        self.notebook.append_page(
            self.color_page, Gtk.Label(label="Replace text"))


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

        # Automatic numbers title
        aut_num_title = Gtk.Label(
            label='Automatic numbers templates',
            halign=Gtk.Align.START, margin_bottom=12)
        self.pack_start(aut_num_title, True, True, 0)

        # Automatic numbers containers
        aut_num_main_box = Gtk.HBox(halign=Gtk.Align.END, spacing=6)
        self.pack_start(aut_num_main_box, True, True, 0)

        aut_num_labels = Gtk.VBox(spacing=6)
        aut_num_main_box.pack_start(aut_num_labels, True, True, 0)

        aut_num_values = Gtk.VBox(spacing=6)
        aut_num_main_box.pack_start(aut_num_values, True, True, 0)

        # 1, 2, 3
        label_1 = Gtk.Label('1, 2, 3 ', halign=Gtk.Align.END)
        label_1.set_sensitive(False)
        aut_num_labels.pack_start(label_1, True, True, 0)

        self.entry_1 = EntryMarkup(halign=Gtk.Align.END)
        aut_num_values.pack_start(self.entry_1, True, True, 0)
        self.entry_1.set_text(self.markup_settings['[1, 2, 3]'][1:-1])

        # 01, 02, 03
        label_01 = Gtk.Label('01, 02, 03 ', halign=Gtk.Align.END)
        label_01.set_sensitive(False)
        aut_num_labels.pack_start(label_01, True, True, 0)

        self.entry_01 = EntryMarkup(halign=Gtk.Align.END)
        aut_num_values.pack_start(self.entry_01, True, True, 0)
        self.entry_01.set_text(self.markup_settings['[01, 02, 03]'][1:-1])

        # 001, 002, 003
        label_001 = Gtk.Label('001, 002, 003 ', halign=Gtk.Align.END)
        label_001.set_sensitive(False)
        aut_num_labels.pack_start(label_001, True, True, 0)

        self.entry_001 = EntryMarkup(halign=Gtk.Align.END)
        aut_num_values.pack_start(self.entry_001, True, True, 0)
        self.entry_001.set_text(self.markup_settings['[001, 002, 003]'][1:-1])

        # Original filename
        orig_filename_title = Gtk.Label(
            label='Original filename template',
            halign=Gtk.Align.START, margin_top=18, margin_bottom=12)
        self.pack_start(orig_filename_title, True, True, 0)

        # Original filename container
        orig_filename_box = Gtk.HBox(halign=Gtk.Align.END, spacing=6)
        self.pack_start(orig_filename_box, True, True, 0)

        label_orig_filename = Gtk.Label(
            label='Original filename', halign=Gtk.Align.END)
        label_orig_filename.set_sensitive(False)
        orig_filename_box.pack_start(label_orig_filename, True, True, 0)

        self.entry_filename = EntryMarkup(halign=Gtk.Align.END)
        orig_filename_box.pack_start(self.entry_filename, True, True, 0)
        self.entry_filename.set_text(self.markup_settings['[original-name]'][1:-1])


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


class EntryMarkup(Gtk.HBox):
    """docstring for TemplatesMarkup"""
    def __init__(self, *args, **kwargs):
        Gtk.HBox.__init__(self, spacing=6, *args, **kwargs)
        self.pack_start(Gtk.Label(label='['), True, True, 0)

        self.entry = Gtk.Entry()
        self.pack_start(self.entry, True, True, 0)

        self.pack_start(Gtk.Label(label=']'), True, True, 0)

    def set_text(self, text: str):
        self.entry.set_text(text)

        


