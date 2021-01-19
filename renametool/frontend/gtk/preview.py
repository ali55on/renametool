import threading

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib

import backend.rename as rename
import backend.replacepreview as replace_preview


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

        # Temp var to compare
        self.rename_text_tmp = self.header.get_text()
        self.search_text_tmp = self.header.get_existing_text()
        self.replace_text_tmp = self.header.get_replace_text()
        self.first_update = True

        # Iniciar pré visualização
        thread = threading.Thread(target=self.preview_threading)
        thread.daemon = True
        thread.start()

    def preview_threading(self):
        GLib.idle_add(self.preview_gtk_glib)
        GLib.timeout_add(300, self.preview_threading)

    def preview_gtk_glib(self):
        # Rename
        if self.header.get_page() == 'rename':
            # Saved variable. Run the method only once
            rename_text = self.header.get_text()
            # Compare whether the text has been updated
            if rename_text != self.rename_text_tmp or self.first_update:
                # Update temporary comparison variable
                self.rename_text_tmp = rename_text
                self.first_update = False

                # Run the preview
                self.rename_preview(rename_text=rename_text)

        # Replace
        else:
            # Saved variable. Run the method only once
            search_text = self.header.get_existing_text()
            replace_text = self.header.get_replace_text()

            # Compare whether the text has been updated
            cond = [
                search_text != self.search_text_tmp,
                replace_text != self.replace_text_tmp
            ]
            if any(cond):

                # Update temporary comparison variable
                self.search_text_tmp = search_text
                self.replace_text_tmp = replace_text

                # Run the preview
                self.replace_preview(
                    search_text=search_text, replace_text=replace_text)

    def rename_preview(self, rename_text: str):
        print('Rename')
        list_store = Gtk.ListStore(str, str)
        if not rename_text:
            rename_text = markup_template['[original-name]']

        rename_status = rename.Rename(
            list_files=self.list_files, new_name=rename_text)
        """
        if rename_status.get_resume_error():
            print('ERROR:', rename_status.get_resume_error())
        if rename_status.get_resume_warning():
            print('WARNING:', rename_status.get_resume_warning())
        """

        for i in self.list_files:
            list_store.append([i.get_original_name() + i.get_extension(), i.get_name() + i.get_extension()])
        self.tree_view.set_model(list_store)

    def replace_preview(self, search_text: str, replace_text: str):
        print('Replace')
        list_store = Gtk.ListStore(str, str)

        if not search_text:
            replace_text = ''

        """replace_status = replace.Replace(
            list_files=self.list_files, search_text=search_text, replace_text=replace_text)"""

        replace_status = replace_preview.ReplacePreview(
            list_files=self.list_files, search_text=search_text, replace_text=replace_text)
        list_match = replace_status.get_match_list()
        list_replace = replace_status.get_replace_list()
        """
        if replace_status.get_resume_error():
            print('ERROR:', replace_status.get_resume_error())
        if replace_status.get_resume_warning():
            print('WARNING:', replace_status.get_resume_warning())
        """
        for m, r in zip(list_match, list_replace):
            list_store.append([m, r])
        self.tree_view.set_model(list_store)
