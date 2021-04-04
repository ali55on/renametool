#!/usr/bin/env python3
import threading
import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

from ui.preferences import PreferencesWindow


class Footer(Gtk.VBox):
    """Program footer

    Contains the program's 'Rename', 'Cancel' and 'Preferences'
    buttons, and above the buttons contains an error notification
    area that is visible only when necessary.
    """
    def __init__(
            self, preview, color_settings, file_list,
            transient, *args, **kwargs) -> None:
        """Class constructor

        Initializes the program's footer widgets.

        :param preview: An inherited 'Gtk.Widget' called 'Preview'
        :param color_settings: A 'dictionary' with color settings
        :param file_list: Python 'list' of 'File' objects
        :param transient: Parent 'Gtk.Window'
        """
        Gtk.VBox.__init__(
            self, margin=18, margin_top=6, spacing=6, *args, **kwargs)
        # Args
        self.preview = preview
        self.color_settings = color_settings
        self.file_list = file_list
        self.transient = transient

        # Flags
        self.can_rename = False

        # Warnings box
        self.warning_box = Gtk.HBox(homogeneous=True)
        self.pack_start(self.warning_box, True, True, 0)

        # Warning - Warning
        self.label_warning = Gtk.Label(
            use_markup=True, ellipsize=3, halign=Gtk.Align.START)
        self.warning_box.pack_start(self.label_warning, True, True, 0)

        # Warning - Error
        self.label_error = Gtk.Label(
            use_markup=True, ellipsize=3, halign=Gtk.Align.START)
        self.warning_box.pack_start(self.label_error, True, True, 0)

        # Style
        self.label_warning.set_name('label-warning')
        self.label_error.set_name('label-error')
        css = b'''
            #label-warning{
                border-bottom: 1px solid #b8b445;
                padding: 3px;
            }
            #label-error{
                border-bottom: 1px solid #c33348;
                padding: 3px;
            }
            '''
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Buttons
        self.buttons_base_box = Gtk.HBox(
            homogeneous=True, valign=Gtk.Align.END)
        self.pack_start(self.buttons_base_box, True, True, 0)

        # Preferences
        self.buttons_incon_box = Gtk.HBox(
            spacing=6, homogeneous=True, halign=Gtk.Align.START)
        self.buttons_base_box.pack_start(self.buttons_incon_box, True, True, 0)

        self.icon_preferences = Gtk.Image(
            icon_name='preferences-other-symbolic')
        self.button_preferences = Gtk.Button(
            image=self.icon_preferences, always_show_image=True,
            tooltip_text='Preferences')
        self.button_preferences.connect('clicked', self.__on_preferences)
        self.buttons_incon_box.pack_start(
            self.button_preferences, True, True, 0)

        # Cancel and rename
        self.buttons_box = Gtk.HBox(spacing=6, homogeneous=True)
        self.buttons_base_box.pack_start(self.buttons_box, True, True, 0)

        self.button_cancel = Gtk.Button(label='Cancel')
        self.button_cancel.connect('clicked', self.__on_cancel)
        self.buttons_box.pack_start(self.button_cancel, True, True, 0)

        self.button_rename = Gtk.Button(label='Rename', can_default=True)
        self.button_rename.connect('clicked', self.__on_rename)
        self.buttons_box.pack_start(self.button_rename, True, True, 0)

        # self.activate_focus()
        # self.set_focus(self.button_rename)
        self.button_rename.set_can_focus(True)
        self.button_rename.set_receives_default(True)
        self.button_rename.get_style_context().add_class('suggested-action')

        # Messages
        self.message = {
            'completely-unnamed': 'Unnamed file',
            'repeated-name-error': 'More than one file with the same name',
            'character-error': 'The slash character is not allowed in the filename',
            'name-not-allowed-error': 'One dot or two dots are not allowed as filenames',
            'existing-name-error': 'Filename already exists in the directory',
            'length-error': 'Filename too long',
            'hidden-file-error': 'Files that the name starts with a dot will be hidden'}

        # Iniciar pré visualização
        thread = threading.Thread(target=self.__status_error_threading)
        thread.daemon = True
        thread.start()

    def set_file_list(self, file_list: list) -> None:
        """Set the file list

        Makes the file list the one passed in the parameter.

        :param file_list: Python 'list' of 'File' objects 
        """
        self.file_list = file_list

    def __on_preferences(self, widget) -> None:
        # Opens the preferences window
        preferences_win = PreferencesWindow(transient_for=self.transient)
        preferences_win.show_all()

    def __on_rename(self, widget) -> None:
        # Renames files
        if self.can_rename:
            for file in self.file_list:
                path = file.get_path()
                ext = file.get_extension()
                old_name = path + file.get_original_name() + ext
                new_name = path + file.get_name() + ext

                if new_name != old_name:
                    os.rename(old_name, new_name)
            Gtk.main_quit()
            exit(0)

    def __on_cancel(self, widget) -> None:
        # Cancels exiting the program
        Gtk.main_quit()
        exit(1)

    def __status_error_threading(self) -> None:
        # Starts daemon that maps errors to the new name entered
        GLib.idle_add(self.__status_error_threading_glib)
        GLib.timeout_add(300, self.__status_error_threading)

    def __status_error_threading_glib(self) -> None:
        # Maps errors to the new name entered
        status_error = self.preview.status_error
        sensitive = self.button_rename.get_sensitive()
        visible_war = self.label_warning.get_visible()
        visible_err = self.label_error.get_visible()

        if status_error:
            if status_error != 'hidden-file-error':
                prefix = '<span color="{}">→</span>  '.format(
                    self.color_settings['error-color'])
                self.label_error.set_markup(
                    prefix + self.message[status_error])
                self.can_rename = False

                if not visible_err:
                    self.label_error.set_visible(True)
                if visible_war:
                    self.label_warning.set_visible(False)

                if sensitive:
                    self.button_rename.set_sensitive(False)
            elif status_error == 'hidden-file-error':
                prefix = '<span color="{}">→</span>  '.format(
                    self.color_settings['warning-color'])
                self.label_warning.set_markup(
                    prefix + self.message[status_error])
                self.can_rename = True

                if not visible_war:
                    self.label_warning.set_visible(True)
                if visible_err:
                    self.label_error.set_visible(False)

                if not sensitive:
                    self.button_rename.set_sensitive(True)
        else:
            if not self.file_list:
                self.button_rename.set_sensitive(False)
                self.can_rename = False
            else:
                self.can_rename = True
                if not sensitive:
                    self.button_rename.set_sensitive(True)
            if visible_war:
                self.label_warning.set_visible(False)
            if visible_err:
                self.label_error.set_visible(False)