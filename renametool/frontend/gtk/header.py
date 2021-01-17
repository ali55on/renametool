import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk

import frontend.gtk.utils.hackstring as hack_string


class StackHeader(Gtk.VBox):
    """"""
    def __init__(self, *args, **kwargs):
        """"""
        Gtk.VBox.__init__(
            self, spacing=6, valign=Gtk.Align.START, halign=Gtk.Align.CENTER,
            width_request=550, *args, **kwargs)
        # Current page flag
        self.current_page = 'rename'

        # Hacking
        hack_str = hack_string.SameSizeString(
            first_str='Rename using a template',
            last_str='Search and replace text')

        # Create Stack
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
        self.stack.set_transition_duration(300)
        # Set "rename" Stack-Page
        self.page_rename = PageRename()
        self.stack.add_titled(self.page_rename, 'rename', hack_str.get_first_str())
        # Set "replace" Stack-Page
        self.page_replace = PageReplace()
        self.stack.add_titled(self.page_replace, 'replace', hack_str.get_last_str())

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

    def get_page(self):
        """"""
        return self.current_page

    def get_text(self):
        """"""
        return self.page_rename.get_text()

    def get_existing_text(self):
        """"""
        return self.page_replace.get_existing_text()

    def get_replace_text(self):
        """"""
        return self.page_replace.get_replace_text()

    # noinspection PyUnusedLocal
    def __set_page(self, widget, data):
        self.current_page = self.stack_switcher.get_stack().get_visible_child_name()


class PageRename(Gtk.VBox):
    """"""
    def __init__(self, *args, **kwargs):
        """"""
        # hig 18px: 12 + 6(spacing) = 18
        Gtk.VBox.__init__(
            self, spacing=6, valign=Gtk.Align.START, margin_top=12, *args, **kwargs)

        self.text_box = Gtk.HBox()
        self.pack_start(self.text_box, True, True, 0)

        self.entry = Gtk.Entry(margin_start=50)
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
        css = b"""
            #entry{
                border-top-right-radius: 0px;
                border-bottom-right-radius: 0px;
            }
            #button{
                border-top-left-radius: 0px;
                border-bottom-left-radius: 0px;
                border-left: 0px;
            }
            """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    @staticmethod
    def __on_menu(widget):
        Popover(widget)

    def get_text(self):
        """"""
        return self.entry.get_text()


class PageReplace(Gtk.HBox):
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
        self.label_box.pack_start(self.search_label, True, True, 0)

        self.search_entry = Gtk.Entry()
        self.entry_box.pack_start(self.search_entry, True, True, 0)

        # Replace
        self.replace_label = Gtk.Label(label='Replace with', halign=Gtk.Align.END)
        self.label_box.pack_start(self.replace_label, True, True, 0)

        self.replace_entry = Gtk.Entry()
        self.entry_box.pack_start(self.replace_entry, True, True, 0)

        # Style
        self.search_label.set_name('search-label')
        self.replace_label.set_name('replace-label')
        css = b"""
            #search-label{
                opacity: 0.5;
            }
            #replace-label{
                opacity: 0.5;
            }
            """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def get_existing_text(self):
        """"""
        return self.search_entry.get_text()

    def get_replace_text(self):
        """"""
        return self.replace_entry.get_text()


class Popover(Gtk.Popover):
    """"""
    def __init__(self, widget, *args, **kwargs):
        """"""
        Gtk.Popover.__init__(self, *args, **kwargs)

        vbox = Gtk.VBox()
        vbox.pack_start(Gtk.ModelButton(label="Item 1"), False, True, 10)
        vbox.pack_start(Gtk.Label(label="Item 2"), False, True, 10)
        vbox.show_all()
        self.add(vbox)
        self.set_position(Gtk.PositionType.BOTTOM)
        self.set_relative_to(widget)
        self.show_all()
        self.popup()
