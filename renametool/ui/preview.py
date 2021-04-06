#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk

from tools.rename import Rename
from tools.replace import Replace
from tools.settings import UserSettings


settings = UserSettings()


class Preview(Gtk.VBox):
    """Preview Box

    List with preview of changes to file names.
    """
    def __init__(self, header, file_list, *args, **kwargs) -> None:
        """Class constructor

        Initializes Preview widgets.

        :param header: Program header (Gtk.Widget/Gtk.Box) object
        :param color_settings: A 'dictionary' with color settings
        :param markup_settings: A 'dictionary' with markup settings
        :param file_list: Python 'list' of 'File' objects
        """
        Gtk.VBox.__init__(self, *args, **kwargs)
        # Args
        self.header = header
        self.file_list = file_list
        self.status_error = None

        # Settings
        self.markup_settings = settings.get_markup_settings()
        self.color_settings = settings.get_color_settings()

        # Scrolled Window
        self.scrolled_window = Gtk.ScrolledWindow(
            propagate_natural_height=True, propagate_natural_width=True)
        self.pack_start(self.scrolled_window, True, True, 0)

        # Box preview
        self.box_preview = Gtk.VBox(homogeneous=True, height_request=300)
        self.scrolled_window.add(self.box_preview)

        # TreeView
        # O ListStore será adicionada na função do preview
        self.tree_view = Gtk.TreeView(
            headers_visible=False, enable_grid_lines=1)
        self.box_preview.pack_start(self.tree_view, True, True, 0)

        # Cell Render - left
        self.cell_renderer_0 = Gtk.CellRendererText(ellipsize=3)
        self.tree_view_column_0 = Gtk.TreeViewColumn(
            None, self.cell_renderer_0, markup=0)
        self.tree_view_column_0.set_expand(True)
        self.tree_view.append_column(self.tree_view_column_0)

        # Cell Render - right
        self.cell_renderer_1 = Gtk.CellRendererText(ellipsize=3)
        self.tree_view_column_1 = Gtk.TreeViewColumn(
            None, self.cell_renderer_1, markup=1)
        self.tree_view_column_1.set_expand(True)
        self.tree_view.append_column(self.tree_view_column_1)

        # Vars for comparison
        self.prev_rename_text = self.header.get_rename_text()
        self.prev_existing_text = self.header.get_existing_text()
        self.prev_replace_text = self.header.get_replace_text()
        self.active_stack_name = self.header.get_active_stack_name()
        self.is_the_first_preview_loop = True

        # Error and Warning color
        self.error_color = self.color_settings['error-color']
        self.warning_color = self.color_settings['warning-color']

        # Arrows
        self.arrow_character  = '→'

        self.error_arrow = '   <span color="{}">{}</span> '.format(
            self.error_color, self.arrow_character)
        
        self.warning_arrow = '   <span color="{}">{}</span> '.format(
            self.warning_color, self.arrow_character)
        
        self.normal_arrow = '   {} '.format(self.arrow_character)
        
        if self.file_list:
            self.__preview_daemon()

    def __preview_daemon(self):
        # Starts the preview daemon
        GLib.idle_add(self.__change_preview_gtk_widgets)
        GLib.timeout_add(300, self.__preview_daemon)

    def __change_preview_gtk_widgets(self):
        # Change preview Gtk.Widgets
        # Rename stack
        if self.header.get_active_stack_name() == 'rename':
            rename_text = self.header.get_rename_text()

            if self.__can_update_rename_preview(rename_text=rename_text):
                self.__update_rename_preview(rename_text=rename_text)

        # Replace stack
        else:
            search_text = self.header.get_existing_text()
            replace_text = self.header.get_replace_text()

            if self.__can_update_replace_preview(
                    search_text=search_text, replace_text=replace_text):
                self.__update_replace_preview(
                    search_text=search_text, replace_text=replace_text)

    def __can_update_rename_preview(self, rename_text: str) -> bool:
        # If can update Rename-Stack preview
        condition = [
            # Check if the Gtk.Entry text is new updated text
            rename_text != self.prev_rename_text,
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

    def __can_update_replace_preview(
            self, search_text: str, replace_text: str) -> bool:
        # If can update Replace-Stack preview
        condition = [
            # Check if the Gtk.Entry text
            search_text != self.prev_existing_text,
            replace_text != self.prev_replace_text,  # is new updated text
            self.header.get_active_stack_name() != self.active_stack_name]
            
        if any(condition):  # Update information
            if search_text != self.prev_existing_text:
                self.prev_existing_text = search_text

            if replace_text != self.prev_replace_text:
                self.prev_replace_text = replace_text

            if self.header.get_active_stack_name() != self.active_stack_name:
                self.active_stack_name = self.header.get_active_stack_name()
            
            return True

        return False

    def __update_rename_preview(self, rename_text: str):
        # Updates the preview linked to the 'Rename' stack 
        # Create ListStore
        list_store = Gtk.ListStore(str, str)

        # Fix text ''
        if not rename_text:
            rename_text = self.markup_settings['[original-name]']

        # Rename files
        rename_status = Rename(
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

            old_name = i.get_original_name() + i.get_extension() + '   '
            typed_name = i.get_name() + i.get_extension()

            # Error
            if note and note != 'hidden-file-error' and note == error_found:
                list_store.append([old_name, self.error_arrow + typed_name])

            # Warning
            elif note and note == 'hidden-file-error' and note == error_found:
                list_store.append([old_name, self.warning_arrow + typed_name])

            # Normal
            else:
                list_store.append([old_name, self.normal_arrow + typed_name])

        # Set TreeView model
        self.tree_view.set_model(list_store)

    def __update_replace_preview(self, search_text: str, replace_text: str):
        # Updates the preview linked to the 'Replace' stack 
        # Create ListStore
        list_store = Gtk.ListStore(str, str)

        # Fix text ''
        if not search_text:
            replace_text = ''

        # Rename/Replace files
        replace_status = Replace(
            file_list=self.file_list, search_text=search_text,
            replace_text=replace_text)
        error_found = replace_status.get_error_found()

        # Check errors
        if error_found:
            self.status_error = replace_status.get_error_found()
            print('ERROR:', replace_status.get_error_found())
        else:
            self.status_error = None

        # Matching colors prefix
        old_color = '<span background="{}">'.format(
            self.color_settings['old-matching-color'])
        new_color = '<span background="{}">'.format(
            self.color_settings['new-matching-color'])
        end_color = '</span>'

        # Config ListStore
        for file in self.file_list:
            note = file.get_note()

            old_name_match = file.get_original_name().replace(
                search_text, old_color + search_text + end_color)
            old_name = old_name_match + file.get_extension() + '   '

            typed_name_match = file.get_original_name().replace(
                search_text, new_color + replace_text + end_color)
            typed_name = typed_name_match + file.get_extension()

            # Error
            if note and note != 'hidden-file-error' and note == error_found:
                list_store.append([old_name, self.error_arrow + typed_name])
            
            # Warning
            elif note and note == 'hidden-file-error' and note == error_found:
                list_store.append([old_name, self.warning_arrow + typed_name])

            # Normal
            else:
                list_store.append([old_name, self.normal_arrow + typed_name])

        # Set TreeView model
        self.tree_view.set_model(list_store)

    def set_file_list(self, file_list):
        """Set the file list

        Makes the file list the one passed in the parameter.

        :param file_list: Python 'list' of 'File' objects 
        """
        self.file_list = file_list
        self.__preview_daemon()
