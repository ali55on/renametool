#!/usr/bin/env python3
import threading
import time

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib


class StackHeader(Gtk.VBox):
    """Create an object of type 'StackHeader'

    Contains two pages (Gtk.Stack), one to rename and another to replace a
    text. Above the pages there is a change button to switch between them.
    Each of the two pages is a separate object (class).
    """
    def __init__(self, markup_settings, *args, **kwargs) -> None:
        """"""
        Gtk.VBox.__init__(
            self, spacing=6, valign=Gtk.Align.START, halign=Gtk.Align.CENTER,
            width_request=550, margin=18, margin_bottom=0, *args, **kwargs)
        # Args
        self.markup_settings = markup_settings

        # Flags
        self.active_work_stack_name = 'rename'

        # Create Stack
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
        self.stack.set_transition_duration(300)

        # "Rename" Stack-Page
        self.tab_rename = TabRename(markup_settings=self.markup_settings)
        self.stack.add_titled(self.tab_rename, 'rename', 'Rename stack')

        # "Replace" Stack-Page
        self.tab_replace = TabReplace()
        self.stack.add_titled(self.tab_replace, 'replace', 'Replace stack')

        # Set Switch Button on top
        self.box_switch = Gtk.HBox(
            margin_start=50, margin_end=50, spacing=6, halign=Gtk.Align.START)
        self.pack_start(self.box_switch, True, True, 0)

        self.switch = Gtk.Switch()
        self.switch.connect('notify::active', self.__on_switch_activated)
        self.switch.set_active(False)
        self.box_switch.pack_start(self.switch, True, True, 0)

        self.label_switch = Gtk.Label(label='Search and replace text')
        self.box_switch.pack_start(self.label_switch, True, True, 0)

        # Set Stack-Pages on bottom
        self.pack_start(self.stack, True, True, 0)


    def get_active_stack_name(self) -> str:
        """Get active stack name

        When the Gtk.Switch button is disabled, the 'active' page is
        the "rename" page, and when it is activated, the 'active' page is
        the "replace" page. Then returns the string "rename" or "replace".

        :return: String containing the name of the active stack
        """
        return self.active_work_stack_name

    def get_rename_text(self) -> str:
        """Gets the new name entered in the Gtk.Entry

        The text with the markings in the main Gtk.Entry, when
        Gtk.Switch (replace option) is disabled.

        :return: String containing the text of the new name 
        """
        return self.tab_rename.get_rename_text()

    def get_existing_text(self) -> str:
        """Gets the text from the match search

        The search text by correspondence, when GTKSwitch ("search and
        replace text") is activated.

        :return: String containing the search text
        """
        return self.tab_replace.get_existing_text()

    def get_replace_text(self) -> str:
        """Gets the replacement text

        The replacement text, when GTKSwitch ("search and replace text")
        is activated.

        :return: String containing the replacement text
        """
        return self.tab_replace.get_replace_text()

    def __on_switch_activated(self, widget, gparam) -> None:
        # Switch stack
        # == self.stack_switcher.get_stack().get_visible_child_name()
        if self.active_work_stack_name == 'rename':
            self.stack.set_visible_child(self.tab_replace)
            self.active_work_stack_name = 'replace'
        else:
            self.stack.set_visible_child(self.tab_rename)
            self.active_work_stack_name = 'rename'


class TabRename(Gtk.VBox):
    """...

    ...

    """
    def __init__(self, markup_settings, *args, **kwargs) -> None:
        """...

        ...

        :return: ...
        """
        Gtk.VBox.__init__(
            self, spacing=6, valign=Gtk.Align.START, *args, **kwargs)
        # Args
        self.markup_settings = markup_settings

        # Main box
        self.text_box = Gtk.HBox()
        self.pack_start(self.text_box, True, True, 0)

        # Entry - new name
        self.entry = Gtk.Entry(
            text=self.markup_settings['[original-name]'], margin_start=50,
            activates_default=True, editable=True)
        self.entry.connect('backspace', self.on_backspace_signal)
        self.entry.connect("key-press-event", self.on_key_press_event)
        self.text_box.pack_start(self.entry, True, True, 0)

        # Entry button (+ Add)
        self.icon = Gtk.Image(icon_name='list-add-symbolic')
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
            Gdk.Screen.get_default(), style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def __on_menu(self, widget) -> None:
        #
        PopoverMenu(
            parent_widget=widget, interaction_widget=self.entry,
            markup_settings=self.markup_settings)

    # noinspection PyUnusedLocal
    def on_backspace_signal(self, widget) -> None:
        """...

        ...

        :return: ...
        """
        can_delete_template = False
        txt = self.entry.get_text()
        cursor = self.entry.get_position()
        new_txt = str()
        cursor_position = None

        # Delete template markup
        for template in self.markup_settings.values():
            for num in range(1, len(txt) + 1):
                init_text = txt[cursor - num: cursor]
                end_text = txt[cursor:(cursor + len(template)) - num]
                if init_text + end_text == template:
                    # Quando o cursor é movido para a posição correta,
                    # ele (Gtk) "come" um caractere (*), por isso o novo
                    # texto recebe um caractere que será deletado quando o
                    # cursor voltar a posição esperada.
                    new_txt = txt.replace(template, ' ')
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

        # O range() para achar a posição correta do cursor, é feito no texto
        # novo e menor para evitar o erro -> "IndexError: string index out
        # of range". Por essa razão, quando o range chega no fim texto sem
        # achar a diferença, significa que o 'template de marcação' que foi
        # removido, ficava originalmente no fim do texto. Então se o
        # cursor_position não foi configurado (None), significa que ele deveria
        # ficar no fim do texto.
        if cursor_position is None:
            cursor_position = len(new_txt)

        # Set
        if can_delete_template:
            self.entry.set_text(new_txt)
            self.entry.do_move_cursor(
                self.entry, Gtk.MovementStep.LOGICAL_POSITIONS,
                cursor_position, False)

    # noinspection PyUnusedLocal
    def on_key_press_event(self, widget, event) -> None:
        """...

        ...

        :return: ...
        """
        entry_text = self.entry.get_text()
        cursor = self.entry.get_position()
        key = Gdk.keyval_name(event.keyval)
        keys = [
            'BackSpace', 'Right', 'Left', 'Up', 'Down',
            'Control_R', 'Control_L', 'Shift_R', 'Shift_L',
            'Caps_Lock', 'Tab', 'Alt_L', 'ISO_Level3_Shift']

        template_found = None
        if key not in keys:
            for template in self.markup_settings.values():
                for num in range(1, len(entry_text) + 1):
                    init_txt = entry_text[cursor - num: cursor]
                    end_txt = entry_text[cursor:(cursor + len(template)) - num]
                    if init_txt + end_txt == template:
                        template_found = template
                        break

            # Preview threading
            thread = threading.Thread(
                target=self.on_key_press_event_threading,
                args=[template_found])
            thread.daemon = True
            thread.start()

    def on_key_press_event_threading(self, template_found) -> None:
        """...

        ...

        :return: ...
        """
        time.sleep(0.01)
        if template_found and template_found not in self.entry.get_text():
            GLib.idle_add(self.on_key_press_event_threading_glib)

    def on_key_press_event_threading_glib(self) -> None:
        """...

        ...

        :return: ...
        """
        self.entry.do_delete_from_cursor(self.entry, 0, -1)

    def get_rename_text(self) -> str:
        """...

        ...

        :return: ...
        """
        return self.entry.get_text()


class TabReplace(Gtk.HBox):
    """"""
    def __init__(self, *args, **kwargs):
        """"""
        Gtk.HBox.__init__(self, spacing=6, *args, **kwargs)
        # Label box
        self.label_box = Gtk.VBox(spacing=6, margin_start=50)
        self.pack_start(self.label_box, False, True, 0)

        # Entry box
        self.entry_box = Gtk.VBox(spacing=6, margin_end=50)
        self.pack_start(self.entry_box, True, True, 0)

        # Search Label
        self.search_label = Gtk.Label(
            label='Existing text', halign=Gtk.Align.END)
        self.search_label.set_sensitive(False)
        self.label_box.pack_start(self.search_label, True, True, 0)

        # Search Entry
        self.search_entry = Gtk.Entry(activates_default=True)
        self.entry_box.pack_start(self.search_entry, True, True, 0)

        # Replace Label
        self.replace_label = Gtk.Label(
            label='Replace with', halign=Gtk.Align.END)
        self.replace_label.set_sensitive(False)
        self.label_box.pack_start(self.replace_label, True, True, 0)

        # Replace Entry
        self.replace_entry = Gtk.Entry(activates_default=True)
        self.entry_box.pack_start(self.replace_entry, True, True, 0)

    def get_existing_text(self):
        """"""
        return self.search_entry.get_text()

    def get_replace_text(self):
        """"""
        return self.replace_entry.get_text()


class PopoverMenu(Gtk.PopoverMenu):
    """"""
    def __init__(
        self, parent_widget, interaction_widget, markup_settings,
        *args, **kwargs):
        """"""
        Gtk.PopoverMenu.__init__(self, *args, **kwargs)
        # Args
        self.parent_widget = parent_widget
        self.entry_widget = interaction_widget
        self.markup_settings = markup_settings

        # Main box
        self.vbox = Gtk.VBox(margin=12)

        # Automatic numbers title
        self.label_numbers_title = Gtk.Label(label='Automatic numbers')
        self.label_numbers_title.set_sensitive(False)
        self.vbox.pack_start(self.label_numbers_title, True, True, 0)

        # Button - Automatic numbers 1, 2, 3
        self.button_1 = Gtk.ModelButton(
            label=self.markup_settings['[1, 2, 3]'][1:-1],
            halign=Gtk.Align.START)
        self.button_1.connect('clicked', self.on_button_1)
        self.vbox.pack_start(self.button_1, True, True, 0)

        # Button - Automatic numbers 01, 02, 03
        self.button_01 = Gtk.ModelButton(
            label=self.markup_settings['[01, 02, 03]'][1:-1],
            halign=Gtk.Align.START)
        self.button_01.connect('clicked', self.on_button_01)
        self.vbox.pack_start(self.button_01, True, True, 0)

        # Button - Automatic numbers 001, 002, 003
        self.button_001 = Gtk.ModelButton(
            label=self.markup_settings['[001, 002, 003]'][1:-1],
            halign=Gtk.Align.START)
        self.button_001.connect('clicked', self.on_button_001)
        self.vbox.pack_start(self.button_001, True, True, 0)

        # Separator
        self.vbox.pack_start(
            Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL),
            True, True, 0)

        # Button - Original filename
        self.button_original_name = Gtk.ModelButton(
            label=self.markup_settings['[original-name]'][1:-1],
            halign=Gtk.Align.START)
        self.button_original_name.connect('clicked',
            self.on_button_original_name)
        self.vbox.pack_start(self.button_original_name, True, True, 0)

        # Config PopoverMenu
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
            self.entry_widget, self.markup_settings['[1, 2, 3]'])

    # noinspection PyUnusedLocal
    def on_button_01(self, widget):
        self.entry_widget.do_insert_at_cursor(
            self.entry_widget, self.markup_settings['[01, 02, 03]'])

    # noinspection PyUnusedLocal
    def on_button_001(self, widget):
        self.entry_widget.do_insert_at_cursor(
            self.entry_widget, self.markup_settings['[001, 002, 003]'])

    # noinspection PyUnusedLocal
    def on_button_original_name(self, widget):
        self.entry_widget.do_insert_at_cursor(
            self.entry_widget, self.markup_settings['[original-name]'])

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
            self.markup_settings['[1, 2, 3]'] in text,
            self.markup_settings['[01, 02, 03]'] in text,
            self.markup_settings['[001, 002, 003]'] in text,
        ]
        if any(con):
            self.__block_num_buttons(block=True)
        else:
            self.__block_num_buttons(block=False)

        # Original name
        if self.markup_settings['[original-name]'] in text:
            self.button_original_name.set_sensitive(False)
        else:
            self.button_original_name.set_sensitive(True)
