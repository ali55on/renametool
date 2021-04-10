#!/usr/bin/env python3
import os

import cairo
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

from tools.utils.file import File


class RenameFile(Gtk.Window):
    def __init__(self, file: str, *args, **kwargs):
        Gtk.Window.__init__(self, default_height=5, default_width=5, *args, *kwargs)
        self.set_keep_below(True)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_type_hint(5)

        # Args
        self.file = File(file)
        self.file_path = self.file.get_path()
        self.file_name = self.file.get_name()
        self.file_extension = self.file.get_extension()

        # Container
        self.container_box = Gtk.VBox(
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
        )
        self.add(self.container_box)

        # Top
        self.top_box = Gtk.HBox(
            margin=12,
            margin_top=6,
            margin_bottom=6,
            spacing=6)
        self.container_box.pack_start(self.top_box, True, True, 0)

        # Label
        self.label = Gtk.Label(
            label='Filename',
            halign=Gtk.Align.START)
        self.top_box.pack_start(self.label, True, True, 0)

        # Image
        self.icon = Gtk.Image(icon_name='window-close-symbolic')

        # Close
        self.button_close = Gtk.Button(
            image=self.icon,
            always_show_image=True,
            halign=Gtk.Align.END,
            relief=Gtk.ReliefStyle.NONE)
        self.button_close.connect('clicked', self.__on_exit)
        self.top_box.pack_start(self.button_close, True, True, 0)

        # Base
        self.base_box = Gtk.HBox(
            margin=12,
            margin_top=0,
            spacing=6)
        self.container_box.pack_start(self.base_box, True, True, 0)

        # Entry
        self.entry = Gtk.Entry(width_chars=25, activates_default=True)
        self.base_box.pack_start(self.entry, True, True, 0)
        self.entry.set_text(
            '{}{}'.format(
                self.file_name,
                self.file_extension))

        # Button
        self.button = Gtk.Button(label='Rename', can_default=True)
        self.button.connect('clicked', self.__on_button_clicked)
        self.base_box.pack_start(self.button, True, True, 0)

        # Default button
        self.activate_default()
        self.set_default(self.button)
        self.button.get_style_context().add_class('suggested-action')

        # Focus
        self.activate_focus()
        self.set_focus(self.entry)

        # Opacity
        self.opacity_screen = self.get_screen()
        self.opacity_visual = self.opacity_screen.get_rgba_visual()
        if self.opacity_visual:
            if self.opacity_screen.is_composited():
                self.set_visual(self.opacity_visual)

        self.set_app_paintable(True)
        self.connect('draw', self.draw)
        self.show_all()

        # Css
        self.container_box.set_name('container-box')
        self.button_close.set_name('button-close')
        css = b"""
            #container-box {
                background-color: inherit;
                border-radius: 5px;
                }
            #button-close {
                border-radius: 50%;
                }
            """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        GLib.timeout_add(100, self.__select)

    def __select(self):
        self.entry.select_region(0, len(self.file_name))

    def draw(self, widget, context):
        color = '00000088'
        red = int(color[0:2], 16) / 255
        green = int(color[2:4], 16) / 255
        blue = int(color[4:6], 16) / 255
        alpha = int(color[6:8], 16) / 255
        context.set_source_rgba(red, green, blue, alpha)

        context.set_operator(cairo.OPERATOR_SOURCE)
        context.paint()
        context.set_operator(cairo.OPERATOR_OVER)

    def __on_button_clicked(self, widget):
        old_url = self.file.get_url()
        new_url = '{}{}'.format(self.file_path, self.entry.get_text())

        os.rename(old_url, new_url)
        self.__on_exit()

    def __on_exit(self, *args, **kwargs):
        Gtk.main_quit()


if __name__ == '__main__':
    win = RenameFile('test')
    win.connect('destroy', Gtk.main_quit)
    win.show_all()
    win.fullscreen()
    Gtk.main()