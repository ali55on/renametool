#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from tools.utils.file import File


class SelectFiles(Gtk.VBox):
    """docstring for EmptyStartWindow"""
    def __init__(self, file_list, *args, **kwargs):
        Gtk.VBox.__init__(self, height_request=300, *args, **kwargs)

        # Flag
        self.file_list = file_list
        self.can_update_list = False

        # Choose Files Box
        self.box_choose_files = Gtk.HBox(spacing=6, valign=Gtk.Align.CENTER, halign=Gtk.Align.CENTER)
        self.pack_start(self.box_choose_files, True, True, 0)

        # Choose Files Label
        self.label_choose_files = Gtk.Label(label='Choose files to rename')
        self.box_choose_files.pack_start(self.label_choose_files, True, True, 0)

        # Choose Files Button # FileChooserButton
        self.icon_open = Gtk.Image(icon_name='folder-open-symbolic')
        self.button_choose_files = Gtk.Button(image=self.icon_open, always_show_image=True)
        self.button_choose_files.connect('clicked', self.__on_select_files)
        self.box_choose_files.pack_start(self.button_choose_files, True, True, 0)

    def __on_select_files(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", 
            action=Gtk.FileChooserAction.OPEN, select_multiple=True)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK)

        response = dialog.run()
        
        if response != Gtk.ResponseType.CANCEL:
            self.file_list = list(File(x) for x in dialog.get_uris())

        dialog.destroy()

    def get_file_list(self):
        return self.file_list
