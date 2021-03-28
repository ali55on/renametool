#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class EmptyWindow(Gtk.Window):
    """docstring for EmptyStartWindow"""
    def __init__(self):
        Gtk.Window.__init__(
            self, title='RenameTool', window_position=Gtk.WindowPosition.CENTER,
            icon_name='document-edit-symbolic', width_request=500)

        # Flag
        self.ok = False
        self.file_list = list()

        # Container
        self.box = Gtk.VBox(margin=18, spacing=18)
        self.add(self.box)

        # Choose Files Box
        self.box_choose_files = Gtk.HBox(spacing=6, valign=Gtk.Align.START, halign=Gtk.Align.START)
        self.box.pack_start(self.box_choose_files, True, True, 0)

        # Choose Files Label
        self.label_choose_files = Gtk.Label(label='Choose files to rename')
        self.box_choose_files.pack_start(self.label_choose_files, True, True, 0)

        # Choose Files Button
        self.icon_open = Gtk.Image(icon_name='folder-open-symbolic')
        self.button_choose_files = Gtk.Button(image=self.icon_open, always_show_image=True)
        self.button_choose_files.connect('clicked', self.on_select_files)
        self.box_choose_files.pack_start(self.button_choose_files, True, True, 0)

        # Text
        self.scrolledwindow = Gtk.ScrolledWindow(min_content_height=300)
        self.scrolledwindow.set_hexpand(True)
        self.scrolledwindow.set_vexpand(True)

        self.textview = Gtk.TextView(top_margin=10, left_margin=10, right_margin=10)
        self.textbuffer = self.textview.get_buffer()
        self.scrolledwindow.add(self.textview)

        self.box.pack_start(self.scrolledwindow, True, True, 0)
        self.scrolledwindow.set_sensitive(False)

        # Base
        self.box_base = Gtk.HBox(spacing=6)
        self.box.pack_start(self.box_base, True, True, 0)

        self.button_cancel = Gtk.Button(label='Cancel')
        self.button_cancel.connect('clicked', self.on_cancel_button)
        self.box_base.pack_start(self.button_cancel, True, True, 0)

        self.button_ok = Gtk.Button(label='Ok')
        self.button_ok.connect('clicked', self.on_ok_button)
        self.box_base.pack_start(self.button_ok, True, True, 0)
        self.button_ok.set_sensitive(False)
        
        # End
        self.connect("destroy", self.quit)
        self.show_all()
        Gtk.main()

    def on_select_files(self, widget):
        # Clear
        self.textbuffer.set_text('')

        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self, 
            action=Gtk.FileChooserAction.OPEN, select_multiple=True,
            local_only=True)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK)

        response = dialog.run()
        print(type(response))
        if response != Gtk.ResponseType.CANCEL:
            self.file_list = dialog.get_uris()

            self.scrolledwindow.set_sensitive(True)
            if self.file_list:
                self.button_ok.set_sensitive(True)
                for item in self.file_list:
                    self.textbuffer.insert_at_cursor(item + '\n')
        else:
            self.file_list = list()
            self.button_ok.set_sensitive(False)
            self.scrolledwindow.set_sensitive(False)

        dialog.destroy()

    def get_file_list(self):
        return self.file_list

    def on_ok_button(self, widget):
        self.ok = True
        self.destroy()

    def on_cancel_button(self, widget):
        self.file_list = list()
        self.destroy()

    def quit(self, widget):
        if not self.ok:
            self.file_list = list()
        Gtk.main_quit()
