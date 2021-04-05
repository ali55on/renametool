#!/usr/bin/env python3
import os
from gi.repository import Nautilus, GObject


class RenameToolNautilusExtension(GObject.GObject, Nautilus.MenuProvider):
    """"""
    def get_file_items(self, window, files):
        menuitem = Nautilus.MenuItem(
            name='RenameTool::rename_tool',
            label='Rename tool',
            tip='Rename tool',
            icon='')

        menuitem.connect('activate', self.on_menu_item_clicked, files)
        return menuitem,

    def on_menu_item_clicked(self, item, files):
        cmd = 'renametool'
        for f in files:
            cmd += ' {}'.format(f.get_uri())

        os.system(cmd)
