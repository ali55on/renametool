import threading
import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib


class Base(Gtk.VBox):
    def __init__(self, list_files, preview, *args, **kwargs):
        """"""
        Gtk.VBox.__init__(self, margin=18, margin_top=12, spacing=6, *args, **kwargs)
        self.list_files = list_files
        self.preview = preview
        self.can_rename = False

        # Warnings
        self.warning_box = Gtk.HBox()
        self.pack_start(self.warning_box, True, True, 0)

        self.label_warning = Gtk.Label(use_markup=True, ellipsize=3, halign=Gtk.Align.START)
        self.warning_box.pack_start(self.label_warning, True, True, 0)

        # Buttons
        self.buttons_base_box = Gtk.HBox(homogeneous=True)
        self.pack_start(self.buttons_base_box, True, True, 0)

        # Preferences
        self.icon = Gtk.Image(icon_name='preferences-system-symbolic')
        self.button_settings = Gtk.Button(
            image=self.icon, always_show_image=True, halign=Gtk.Align.START)
        self.button_settings.connect('clicked', self.on_cancel)
        self.buttons_base_box.pack_start(self.button_settings, True, True, 0)

        # Cancel and rename
        self.buttons_box = Gtk.HBox(spacing=6, homogeneous=True)
        self.buttons_base_box.pack_start(self.buttons_box, True, True, 0)

        self.button_cancel = Gtk.Button(label='Cancel')
        self.button_cancel.connect('clicked', self.on_cancel)
        self.buttons_box.pack_start(self.button_cancel, True, True, 0)

        self.button_rename = Gtk.Button(label='Rename', can_default=True)
        self.button_rename.connect('clicked', self.on_rename)
        self.buttons_box.pack_start(self.button_rename, True, True, 0)

        # self.activate_focus()
        # self.set_focus(self.button_ok)
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
        thread = threading.Thread(target=self.status_error_threading)
        thread.daemon = True
        thread.start()

    # noinspection PyUnusedLocal
    def on_rename(self, widget):
        if self.can_rename:
            for file in self.list_files:
                path = file.get_path()
                ext = file.get_extension()

                old_name = path + file.get_original_name() + ext
                new_name = path + file.get_name() + ext
                if new_name != old_name:
                    os.rename(old_name, new_name)
            Gtk.main_quit()

    # noinspection PyUnusedLocal,PyMethodMayBeStatic
    def on_cancel(self, widget):
        Gtk.main_quit()

    def status_error_threading(self):
        GLib.idle_add(self.status_error_threading_glib)
        GLib.timeout_add(300, self.status_error_threading)

    def status_error_threading_glib(self):
        status_error = self.preview.status_error
        sensitive = self.button_rename.get_sensitive()
        visible = self.label_warning.get_visible()

        if status_error:
            if not visible:
                self.label_warning.set_visible(True)
            if status_error != 'hidden-file-error':
                self.label_warning.set_markup(
                    '<span color="#c33348">→</span>: ' + self.message[status_error])
                self.can_rename = False
                if sensitive:
                    self.button_rename.set_sensitive(False)
            elif status_error == 'hidden-file-error':
                self.label_warning.set_markup(
                    '<span color="#b8b445">→</span>: ' + self.message[status_error])
                self.can_rename = True
                if not sensitive:
                    self.button_rename.set_sensitive(True)
        else:
            self.can_rename = True
            if not sensitive:
                self.button_rename.set_sensitive(True)
            if visible:
                self.label_warning.set_visible(False)
