import threading

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib


class Base(Gtk.VBox):
    def __init__(self, list_files, preview, *args, **kwargs):
        """"""
        Gtk.VBox.__init__(self, margin=18, *args, **kwargs)
        self.list_files = list_files
        self.preview = preview
        self.can_rename = False

        # Warnings
        self.warning_box = Gtk.HBox()
        self.pack_start(self.warning_box, True, True, 0)

        self.label_warning = Gtk.Label(use_markup=True)
        self.warning_box.pack_start(self.label_warning, True, True, 0)

        # Buttons
        self.buttons_box = Gtk.HBox()
        self.pack_start(self.buttons_box, True, True, 0)

        self.button_rename = Gtk.Button(label='Rename')
        self.button_rename.connect('clicked', self.rename)
        self.buttons_box.pack_start(self.button_rename, True, True, 0)

        # Iniciar pré visualização
        thread = threading.Thread(target=self.status_error_threading)
        thread.daemon = True
        thread.start()

    def rename(self, widget):
        if self.can_rename:
            for i in self.list_files:
                print(i.get_name() + i.get_extension())

    def status_error_threading(self):
        GLib.idle_add(self.status_error_threading_glib)
        GLib.timeout_add(300, self.status_error_threading)

    def status_error_threading_glib(self):
        status_error = self.preview.status_error
        sensitive = self.button_rename.get_sensitive()

        if status_error:
            if status_error != 'hidden-file-error':
                if sensitive:
                    self.button_rename.set_sensitive(False)
                    self.can_rename = False
            elif status_error == 'hidden-file-error':
                if not sensitive:
                    self.button_rename.set_sensitive(True)
                    self.can_rename = True
        else:
            self.can_rename = True
            if not sensitive:
                self.button_rename.set_sensitive(True)
