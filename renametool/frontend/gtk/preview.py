import threading

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib

import backend.rename as rename
import backend.replace as replace


markup_template = {
    '[1, 2, 3]': '[1, 2, 3]',
    '[01, 02, 03]': '[01, 02, 03]',
    '[001, 002, 003]': '[001, 002, 003]',
    '[original-name]': '[Original filename]'
}


class Preview(Gtk.VBox):
    """"""
    def __init__(self, header, list_files, *args, **kwargs):
        """"""
        Gtk.VBox.__init__(self, *args, **kwargs)
        self.header = header
        self.list_files = list_files

        # Pré visualização
        self.scrolled_window = Gtk.ScrolledWindow(
            propagate_natural_height=True, propagate_natural_width=True)
        self.pack_start(self.scrolled_window, True, True, 0)

        self.box_preview = Gtk.VBox(homogeneous=True, height_request=300)
        self.scrolled_window.add(self.box_preview)

        # TreeView
        # O ListStore será adicionada na função do preview
        self.tree_view = Gtk.TreeView(headers_visible=False, enable_grid_lines=1)
        self.box_preview.pack_start(self.tree_view, True, True, 0)

        self.cell_renderer_0 = Gtk.CellRendererText(ellipsize=3)
        self.tree_view_column_0 = Gtk.TreeViewColumn(None, self.cell_renderer_0, markup=0)
        self.tree_view_column_0.set_expand(True)
        self.tree_view.append_column(self.tree_view_column_0)

        self.cell_renderer_1 = Gtk.CellRendererText(ellipsize=3)
        self.tree_view_column_1 = Gtk.TreeViewColumn(None, self.cell_renderer_1, markup=1)
        self.tree_view_column_1.set_expand(True)
        self.tree_view.append_column(self.tree_view_column_1)

        # Vars for comparison
        self.prev_rename_text = self.header.get_rename_text()
        self.prev_existing_text = self.header.get_existing_text()
        self.prev_replace_text = self.header.get_replace_text()
        self.is_the_first_preview_loop = True

        # Iniciar pré visualização
        thread = threading.Thread(target=self.preview_threading)
        thread.daemon = True
        thread.start()

    def preview_threading(self):
        GLib.idle_add(self.preview_threading_glib)
        GLib.timeout_add(300, self.preview_threading)

    def preview_threading_glib(self):
        # Rename
        if self.header.get_active_work_tab() == 'rename':
            rename_text = self.header.get_rename_text()

            if self.can_update_rename_preview(rename_text=rename_text):
                self.rename_preview(rename_text=rename_text)

        # Replace
        else:  # get_active_work_tab() = 'replace':
            search_text = self.header.get_existing_text()
            replace_text = self.header.get_replace_text()

            if self.can_update_replace_preview(
                    search_text=search_text, replace_text=replace_text):
                self.replace_preview(
                    search_text=search_text, replace_text=replace_text)

    def can_update_rename_preview(self, rename_text: str) -> bool:
        condition = [
            # Check if the Gtk.Entry text is new updated text
            rename_text != self.prev_rename_text,
            self.is_the_first_preview_loop,
            self.header.get_changed_work_tab()
        ]
        if any(condition):
            # Update information
            self.prev_rename_text = rename_text
            self.header.set_changed_work_tab(changed=False)
            self.is_the_first_preview_loop = False
            return True
        return False

    def can_update_replace_preview(self, search_text: str, replace_text: str) -> bool:
        condition = [
            # Check if the Gtk.Entry text is new updated text
            search_text != self.prev_existing_text,
            replace_text != self.prev_replace_text,
            self.header.get_changed_work_tab()
        ]
        if any(condition):
            # Update information
            self.prev_existing_text = search_text
            self.prev_replace_text = replace_text
            self.header.set_changed_work_tab(changed=False)
            return True
        return False

    def rename_preview(self, rename_text: str):
        list_store = Gtk.ListStore(str, str)
        if not rename_text:
            rename_text = markup_template['[original-name]']

        rename_status = rename.Rename(
            list_files=self.list_files, new_name=rename_text)

        if rename_status.get_resume_error():
            print('ERROR:', rename_status.get_resume_error())
        if rename_status.get_resume_warning():
            print('WARNING:', rename_status.get_resume_warning())

        found_a_warning = False
        for i in self.list_files:
            if i.get_note() == 'error' and not found_a_warning:
                found_a_warning = True
                list_store.append(
                    [
                        i.get_original_name() + i.get_extension() + '   ',
                        '  <span background="#ef356444"> → </span> ' + i.get_name() + i.get_extension()
                    ]
                )
            elif i.get_note() == 'warning' and not found_a_warning:
                found_a_warning = True
                list_store.append(
                    [
                        i.get_original_name() + i.get_extension() + '   ',
                        '  <span background="#ffdb5744"> → </span> ' + i.get_name() + i.get_extension()
                    ]
                )
            else:
                list_store.append(
                    [
                        i.get_original_name() + i.get_extension() + '   ',
                        '   → ' + i.get_name() + i.get_extension()
                    ]
                )
        self.tree_view.set_model(list_store)

    def replace_preview(self, search_text: str, replace_text: str):
        list_store = Gtk.ListStore(str, str)

        if not search_text:
            replace_text = ''

        replace_status = replace.Replace(
            list_files=self.list_files, search_text=search_text, replace_text=replace_text)

        if replace_status.get_resume_error():
            print('ERROR:', replace_status.get_resume_error())
        if replace_status.get_resume_warning():
            print('WARNING:', replace_status.get_resume_warning())

        old_color = '<span background="#f9885444">'
        new_color = '<span background="#69a75344">'
        end_color = '</span>'
        found_a_warning = False
        for file in self.list_files:
            old = file.get_original_name().replace(search_text, old_color + search_text + end_color)
            new = file.get_original_name().replace(search_text, new_color + replace_text + end_color)

            if file.get_note() == 'error' and not found_a_warning:
                found_a_warning = True
                list_store.append(
                    [old + file.get_extension() + '   ',
                     '  <span background="#ef356444"> → </span> ' + new + file.get_extension()])
            elif file.get_note() == 'warning' and not found_a_warning:
                found_a_warning = True
                list_store.append(
                    [old + file.get_extension() + '   ',
                     '  <span background="#ffdb5744"> → </span> ' + new + file.get_extension()])
            else:
                list_store.append([old + file.get_extension() + '   ', '   → ' + new + file.get_extension()])
        self.tree_view.set_model(list_store)
