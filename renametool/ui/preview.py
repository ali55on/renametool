#!/usr/bin/env python3
import threading

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib

import tools.rename as rename
import tools.replace as replace


class Preview(Gtk.VBox):
    """"""
    def __init__(self, header, color_settings, markup_settings, file_list, *args, **kwargs):
        """"""
        Gtk.VBox.__init__(self, *args, **kwargs)
        # Args
        self.header = header
        self.color_settings = color_settings
        self.file_list = file_list
        self.markup_settings = markup_settings
        self.status_error = None

        # Flag
        self.preview_daemon = False

        # Scrolled Window
        self.scrolled_window = Gtk.ScrolledWindow(
            propagate_natural_height=True, propagate_natural_width=True)
        self.pack_start(self.scrolled_window, True, True, 0)

        # Box preview
        self.box_preview = Gtk.VBox(homogeneous=True, height_request=300)
        self.scrolled_window.add(self.box_preview)

        # TreeView
        # O ListStore será adicionada na função do preview
        self.tree_view = Gtk.TreeView(headers_visible=False, enable_grid_lines=1)
        self.box_preview.pack_start(self.tree_view, True, True, 0)

        # Cell Render - left
        self.cell_renderer_0 = Gtk.CellRendererText(ellipsize=3)
        self.tree_view_column_0 = Gtk.TreeViewColumn(None, self.cell_renderer_0, markup=0)
        self.tree_view_column_0.set_expand(True)
        self.tree_view.append_column(self.tree_view_column_0)

        # Cell Render - right
        self.cell_renderer_1 = Gtk.CellRendererText(ellipsize=3)
        self.tree_view_column_1 = Gtk.TreeViewColumn(None, self.cell_renderer_1, markup=1)
        self.tree_view_column_1.set_expand(True)
        self.tree_view.append_column(self.tree_view_column_1)

        # Vars for comparison
        self.prev_rename_text = self.header.get_rename_text()
        self.prev_existing_text = self.header.get_existing_text()
        self.prev_replace_text = self.header.get_replace_text()
        self.active_stack_name = self.header.get_active_stack_name()
        self.is_the_first_preview_loop = True

        if self.file_list:
            self.preview_daemon = True
            self.__init_daemon_for_preview()

    def __init_daemon_for_preview(self):
        # Preview threading
        thread = threading.Thread(target=self.preview_threading)
        thread.daemon = True
        thread.start()

    def set_file_list(self, file_list):
        self.file_list = file_list
        if not self.preview_daemon:
            self.__init_daemon_for_preview()

    def preview_threading(self):
        GLib.idle_add(self.preview_threading_glib)
        GLib.timeout_add(300, self.preview_threading)

    def preview_threading_glib(self):
        # Rename
        if self.header.get_active_stack_name() == 'rename':
            rename_text = self.header.get_rename_text()

            if self.can_update_rename_preview(rename_text=rename_text):
                self.rename_preview(rename_text=rename_text)

        # Replace
        else:
            search_text = self.header.get_existing_text()
            replace_text = self.header.get_replace_text()

            if self.can_update_replace_preview(
                    search_text=search_text, replace_text=replace_text):
                self.replace_preview(
                    search_text=search_text, replace_text=replace_text)

    def can_update_rename_preview(self, rename_text: str) -> bool:
        condition = [
            rename_text != self.prev_rename_text,  # Check if the Gtk.Entry text is new updated text
            self.header.get_active_stack_name() != self.active_stack_name,
            self.is_the_first_preview_loop
        ]
        if any(condition):  # Update information
            
            if self.prev_rename_text != rename_text:
                self.prev_rename_text = rename_text

            if self.header.get_active_stack_name() != self.active_stack_name:
                self.active_stack_name = self.header.get_active_stack_name()
            
            if self.is_the_first_preview_loop:
                self.is_the_first_preview_loop = False
            
            return True

        return False

    def can_update_replace_preview(self, search_text: str, replace_text: str) -> bool:
        condition = [
            search_text != self.prev_existing_text,  # Check if the Gtk.Entry text
            replace_text != self.prev_replace_text,  # is new updated text
            self.header.get_active_stack_name() != self.active_stack_name
        ]
        if any(condition):  # Update information
            if search_text != self.prev_existing_text:
                self.prev_existing_text = search_text

            if replace_text != self.prev_replace_text:
                self.prev_replace_text = replace_text

            if self.header.get_active_stack_name() != self.active_stack_name:
                self.active_stack_name = self.header.get_active_stack_name()
            
            return True

        return False

    def rename_preview(self, rename_text: str):
        # Create ListStore
        list_store = Gtk.ListStore(str, str)

        # Fix text ''
        if not rename_text:
            rename_text = self.markup_settings['[original-name]']

        # Rename files
        rename_status = rename.Rename(
            markup_settings=self.markup_settings,
            file_list=self.file_list, new_name=rename_text)
        error_found = rename_status.get_error_found()

        # Check errors
        if error_found:
            self.status_error = rename_status.get_error_found()
            print('ERROR:', rename_status.get_error_found())
        else:
            self.status_error = None

        # Config ListStore
        for i in self.file_list:
            note = i.get_note()
            # Error
            if note and note != 'hidden-file-error' and note == error_found:
                prefix = '   <span color="{}">→</span> '.format(self.color_settings['error-color'])
                list_store.append(
                    [i.get_original_name() + i.get_extension() + '   ',
                     prefix + i.get_name() + i.get_extension()])
            # Warning
            elif note and note == 'hidden-file-error' and note == error_found:
                prefix = '   <span color="{}">→</span> '.format(self.color_settings['warning-color'])
                list_store.append(
                    [i.get_original_name() + i.get_extension() + '   ',
                     prefix + i.get_name() + i.get_extension()])
            else:
                list_store.append(
                    [i.get_original_name() + i.get_extension() + '   ',
                     '   → ' + i.get_name() + i.get_extension()])

        # Set TreeView model
        self.tree_view.set_model(list_store)

    def replace_preview(self, search_text: str, replace_text: str):
        # Create ListStore
        list_store = Gtk.ListStore(str, str)

        # Fix text ''
        if not search_text:
            replace_text = ''

        # Rename/Replace files
        replace_status = replace.Replace(
            file_list=self.file_list, search_text=search_text, replace_text=replace_text)
        error_found = replace_status.get_error_found()

        # Check errors
        if error_found:
            self.status_error = replace_status.get_error_found()
            print('ERROR:', replace_status.get_error_found())
        else:
            self.status_error = None

        # Config ListStore
        old_color = '<span background="{}">'.format(self.color_settings['old-matching-color'])
        new_color = '<span background="{}">'.format(self.color_settings['new-matching-color'])
        end_color = '</span>'
        for file in self.file_list:
            note = file.get_note()
            old = file.get_original_name().replace(search_text, old_color + search_text + end_color)
            new = file.get_original_name().replace(search_text, new_color + replace_text + end_color)
            # Error
            if note and note != 'hidden-file-error' and note == error_found:
                prefix = '   <span color="{}">→</span> '.format(self.color_settings['error-color'])
                list_store.append(
                    [old + file.get_extension() + '   ',
                     prefix + new + file.get_extension()])
            # Warning
            elif note and note == 'hidden-file-error' and note == error_found:
                prefix = '   <span color="{}">→</span> '.format(self.color_settings['warning-color'])
                list_store.append(
                    [old + file.get_extension() + '   ',
                     prefix + new + file.get_extension()])
            else:
                list_store.append([old + file.get_extension() + '   ', '   → ' + new + file.get_extension()])
        # Set TreeView model
        self.tree_view.set_model(list_store)
