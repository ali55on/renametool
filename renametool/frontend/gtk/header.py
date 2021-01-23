import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk

import frontend.gtk.utils.hackstring as hack_string


markup_template = {
    '[1, 2, 3]': '[1, 2, 3]',
    '[01, 02, 03]': '[01, 02, 03]',
    '[001, 002, 003]': '[001, 002, 003]',
    '[original-name]': '[Original filename]'
}


class StackHeader(Gtk.VBox):
    """"""
    def __init__(self, *args, **kwargs):
        """"""
        Gtk.VBox.__init__(
            self, spacing=6, valign=Gtk.Align.START, halign=Gtk.Align.CENTER,
            width_request=550, margin=18, *args, **kwargs)
        # Current page flag
        self.active_work_tab = 'rename'
        self.changed_work_tab = True

        # Hacking
        hack_str = hack_string.SameSizeString(
            first_str='Rename using a template',
            last_str='Search and replace text')

        # Create Stack
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
        self.stack.set_transition_duration(300)
        # Set "rename" Stack-Page
        self.tab_rename = TabRename()
        self.stack.add_titled(self.tab_rename, 'rename', hack_str.get_first_str())
        # Set "replace" Stack-Page
        self.tab_replace = TabReplace()
        self.stack.add_titled(self.tab_replace, 'replace', hack_str.get_last_str())

        # Create Stack-Switcher on top
        self.stack_switcher = Gtk.StackSwitcher(halign=Gtk.Align.CENTER)
        self.stack_switcher.set_stack(self.stack)
        self.pack_start(self.stack_switcher, True, True, 0)
        # Set Stack-Pages on bottom
        self.pack_start(self.stack, True, True, 0)

        # Set current page
        self.stack_switcher.connect('button-release-event', self.__set_page)

        # Style
        self.stack_switcher.set_name('stack-switcher')
        css = b"""
            #stack-switcher{
                font-family: Ubuntu Mono;
            }
            """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def get_active_work_tab(self):
        """"""
        return self.active_work_tab

    def get_changed_work_tab(self):
        """"""
        return self.changed_work_tab

    def set_changed_work_tab(self, changed: bool):
        """"""
        self.changed_work_tab = changed

    def get_rename_text(self):
        """"""
        return self.tab_rename.get_rename_text()

    def get_existing_text(self):
        """"""
        return self.tab_replace.get_existing_text()

    def get_replace_text(self):
        """"""
        return self.tab_replace.get_replace_text()

    # noinspection PyUnusedLocal
    def __set_page(self, widget, data):
        self.active_work_tab = self.stack_switcher.get_stack().get_visible_child_name()
        self.changed_work_tab = True


class TabRename(Gtk.VBox):
    """"""
    def __init__(self, *args, **kwargs):
        """"""
        # hig 18px: 12 + 6(spacing) = 18
        Gtk.VBox.__init__(
            self, spacing=6, valign=Gtk.Align.START, margin_top=12, *args, **kwargs)

        self.text_box = Gtk.HBox()
        self.pack_start(self.text_box, True, True, 0)

        self.entry = Gtk.Entry(
            text=markup_template['[original-name]'], margin_start=50, editable=True)
        self.entry.connect('backspace', self.on_backspace_signal)
        self.text_box.pack_start(self.entry, True, True, 0)

        self.icon = Gtk.Image(icon_name='value-increase-symbolic')

        self.button = Gtk.Button(
            image=self.icon, margin_end=50,
            always_show_image=True, label='Add', halign=Gtk.Align.END)
        self.button.connect('clicked', self.__on_menu)
        self.text_box.pack_start(self.button, False, True, 0)

        # Style
        self.entry.set_name('entry')
        self.button.set_name('button')
        css = b'''
            #entry{
                border-top-right-radius: 0px;
                border-bottom-right-radius: 0px;
            }
            #button{
                border-top-left-radius: 0px;
                border-bottom-left-radius: 0px;
                border-left: 0px;
            }
            '''
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def __on_menu(self, widget):
        PopoverMenu(parent_widget=widget, interaction_widget=self.entry)

    # noinspection PyUnusedLocal
    def on_backspace_signal(self, widget):
        can_delete_template = False
        txt = self.entry.get_text()
        cursor = self.entry.get_position()
        new_txt = str()
        cursor_position = None

        # Delete template markup
        for template in markup_template.values():
            for num in range(1, len(txt) + 1):
                if txt[cursor - num: cursor] + txt[cursor:(cursor + len(template)) - num] == template:
                    # Quando o cursor é movido para a posição correta,
                    # ele (Gtk) "come" um caractere (*), por isso o novo
                    # texto recebe um caractere que será deletado quando o
                    # cursor voltar a posição esperada.
                    new_txt = txt.replace(template, '*')
                    can_delete_template = True
                    break

        # Configure the correct cursor position
        for step in range(len(new_txt)):
            if new_txt[step] != txt[step]:
                # O cursor ganha um incremento de 1
                # unidade, pois quando ele for movido para
                # o lugar correto, ele (Gtk) "comerá"/apagará
                # 1 caractere (*)
                cursor_position = step + 1
                break

        # O range() para achar a posição correta do cursor, é feito no texto novo
        # e menor para evitar o erro -> "IndexError: string index out of range".
        # Por essa razão, quando o range chega no fim texto sem achar a diferença,
        # significa que o 'template de marcação' que foi removido, ficava originalmente
        # no fim do texto. Então se o cursor_position não foi configurado (None),
        # significa que ele deveria ficar no fim do texto
        if cursor_position is None:
            cursor_position = len(new_txt)

        # Set
        if can_delete_template:
            self.entry.set_text(new_txt)
            self.entry.do_move_cursor(
                self.entry, Gtk.MovementStep.LOGICAL_POSITIONS, cursor_position, False)

    def get_rename_text(self):
        """"""
        return self.entry.get_text()


class TabReplace(Gtk.HBox):
    """"""
    def __init__(self, *args, **kwargs):
        """"""
        Gtk.HBox.__init__(self, spacing=6, margin_top=12, *args, **kwargs)
        # Label box
        self.label_box = Gtk.VBox(spacing=6, margin_start=50)
        self.pack_start(self.label_box, False, True, 0)
        # Entry box
        self.entry_box = Gtk.VBox(spacing=6, margin_end=50)
        self.pack_start(self.entry_box, True, True, 0)

        # Search
        self.search_label = Gtk.Label(label='Existing text', halign=Gtk.Align.END)
        self.search_label.set_sensitive(False)
        self.label_box.pack_start(self.search_label, True, True, 0)

        self.search_entry = Gtk.Entry()
        self.entry_box.pack_start(self.search_entry, True, True, 0)

        # Replace
        self.replace_label = Gtk.Label(label='Replace with', halign=Gtk.Align.END)
        self.replace_label.set_sensitive(False)
        self.label_box.pack_start(self.replace_label, True, True, 0)

        self.replace_entry = Gtk.Entry()
        self.entry_box.pack_start(self.replace_entry, True, True, 0)

    def get_existing_text(self):
        """"""
        return self.search_entry.get_text()

    def get_replace_text(self):
        """"""
        return self.replace_entry.get_text()


class PopoverMenu(Gtk.PopoverMenu):
    """"""
    def __init__(self, parent_widget, interaction_widget, *args, **kwargs):
        """"""
        Gtk.PopoverMenu.__init__(self, *args, **kwargs)
        self.parent_widget = parent_widget
        self.entry_widget = interaction_widget

        # Container
        self.vbox = Gtk.VBox(margin=12)

        # Automatic numbers
        self.label_numbers_title = Gtk.Label(label='Automatic numbers')
        self.label_numbers_title.set_sensitive(False)
        self.vbox.pack_start(self.label_numbers_title, True, True, 0)

        # Button 1
        self.button_1 = Gtk.ModelButton(
            label=markup_template['[1, 2, 3]'][1:-1], halign=Gtk.Align.START)
        self.button_1.connect('clicked', self.on_button_1)
        self.vbox.pack_start(self.button_1, True, True, 0)

        # Button 01
        self.button_01 = Gtk.ModelButton(
            label=markup_template['[01, 02, 03]'][1:-1], halign=Gtk.Align.START)
        self.button_01.connect('clicked', self.on_button_01)
        self.vbox.pack_start(self.button_01, True, True, 0)

        # Button 001
        self.button_001 = Gtk.ModelButton(
            label=markup_template['[001, 002, 003]'][1:-1], halign=Gtk.Align.START)
        self.button_001.connect('clicked', self.on_button_001)
        self.vbox.pack_start(self.button_001, True, True, 0)

        # Separator
        self.vbox.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), True, True, 0)

        # Button original-name
        self.button_original_name = Gtk.ModelButton(
            label=markup_template['[original-name]'][1:-1], halign=Gtk.Align.START)
        self.button_original_name.connect('clicked', self.on_button_original_name)
        self.vbox.pack_start(self.button_original_name, True, True, 0)

        self.vbox.show_all()
        self.add(self.vbox)
        self.set_position(Gtk.PositionType.BOTTOM)
        self.set_relative_to(self.parent_widget)
        self.show_all()
        self.popup()

        self.__check_sensitive_buttons()

    # noinspection PyUnusedLocal
    def on_button_1(self, widget):
        self.entry_widget.do_insert_at_cursor(
            self.entry_widget, markup_template['[1, 2, 3]'])

    # noinspection PyUnusedLocal
    def on_button_01(self, widget):
        self.entry_widget.do_insert_at_cursor(
            self.entry_widget, markup_template['[01, 02, 03]'])

    # noinspection PyUnusedLocal
    def on_button_001(self, widget):
        self.entry_widget.do_insert_at_cursor(
            self.entry_widget, markup_template['[001, 002, 003]'])

    # noinspection PyUnusedLocal
    def on_button_original_name(self, widget):
        self.entry_widget.do_insert_at_cursor(
            self.entry_widget, markup_template['[original-name]'])

    def __block_num_buttons(self, block: bool):
        buttons = [self.button_1, self.button_01, self.button_001]
        if block:
            for button in buttons:
                button.set_sensitive(False)
        else:
            for button in buttons:
                button.set_sensitive(True)

    def __check_sensitive_buttons(self):
        # Text
        text = self.entry_widget.get_text()

        # Numbers
        con = [
            markup_template['[1, 2, 3]'] in text,
            markup_template['[01, 02, 03]'] in text,
            markup_template['[001, 002, 003]'] in text,
        ]
        if any(con):
            self.__block_num_buttons(block=True)
        else:
            self.__block_num_buttons(block=False)

        # Original name
        if markup_template['[original-name]'] in text:
            self.button_original_name.set_sensitive(False)
        else:
            self.button_original_name.set_sensitive(True)
