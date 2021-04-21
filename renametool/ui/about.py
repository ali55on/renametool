#!/usr/bin/env python3
import os
import gettext
import locale

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


current_locale, encoding = locale.getdefaultlocale()
path = os.path.dirname(os.path.abspath(__file__))
path_locales = path.replace('ui', 'locales')

t = gettext.translation('about', path_locales, [current_locale])
_ = t.gettext

gettext.install('about')


class AboutWindow(Gtk.Window):
    """About Window

    RenameTool application about window.
    """
    def __init__(self, *args, **kwargs) -> None:
        """Class constructor

        Initializes About Window widgets.
        """
        Gtk.Window.__init__(
            self,
            modal=True,
            type_hint=1, title=_('About'),
            resizable=False, *args, **kwargs)
        # Icon
        icon_url = path.replace('ui', 'data{}rename-tool.svg'.format(os.sep))
        self.set_default_icon_from_file(icon_url)

        # Main container
        self.main_box = Gtk.VBox(margin=12, margin_top=6, spacing=6)
        self.add(self.main_box)

        # Stack
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.OVER_UP_DOWN)
        self.stack.set_transition_duration(300)

        self.about_page = AboutPage()
        self.stack.add_titled(self.about_page, 'about', _('About'))

        self.credit_page = CreditPage()
        self.stack.add_titled(self.credit_page, 'credit', _('Credits'))

        # Stack buttons
        # self.stack_switcher = Gtk.StackSwitcher(
        #     stack=self.stack, halign=Gtk.Align.CENTER)
        # self.main_box.pack_start(self.stack_switcher, True, True, 0)

        # Icon
        self.program_icon = Gtk.Image(file=icon_url, margin=6)
        self.main_box.pack_start(self.program_icon, True, True, 0)

        # Name
        self.program_name = Gtk.Label(use_markup=True)
        self.program_name.set_markup('<b>Rename Tool</b>')
        self.main_box.pack_start(self.program_name, True, True, 0)

        # Stack pages
        self.main_box.pack_start(self.stack, True, True, 0)


class AboutPage(Gtk.VBox):
    """docstring for AboutPage"""
    def __init__(self, *args, **kwargs):
        Gtk.VBox.__init__(self, *args, *kwargs)

        self.license = Gtk.Label(
            use_markup=True,
            justify=Gtk.Justification.CENTER,
            lines=7,
            ellipsize=3,
            max_width_chars=50)

        title = _('Renames multiple files')
        page = _('Web page')
        descript = _('This program comes with ABSOLUTELY NO WARRANTY.')
        details = _('For more details, visit:')

        self.license.set_markup(
            '<small>'
            '{}'
            '\n\n'
            '<a href="https://github.com/w-a-gomes/renametool">{}</a>'
            '\n\n'
            '© 2021  Alisson W.A.Gomes'
            '\n\n'
            '{}\n'
            '{}'
            ' <a href="https://www.gnu.org/licenses/gpl-3.0.html">'
            'GNU General Public License, version 3 or later.'
            '</a>'
            '</small>'.format(
                title, page, descript, details))
        self.pack_start(self.license, True, True, 0)


class CreditPage(Gtk.VBox):
    """docstring for CreditPage"""
    def __init__(self, *args, **kwargs):
        Gtk.VBox.__init__(self, *args, *kwargs)

        self.scroll = Gtk.ScrolledWindow(shadow_type=Gtk.ShadowType.ETCHED_OUT)
        self.pack_start(self.scroll, True, True, 0)

        # Box preview
        self.box_container = Gtk.HBox()
        self.scroll.add(self.box_container)

        # Text view
        self.text_view_label = Gtk.TextView(
            justification=Gtk.Justification.RIGHT)
        self.box_container.pack_start(self.text_view_label, True, True, 0)
        self.text_buffer_label = self.text_view_label.get_buffer()

        self.text_view_value = Gtk.TextView(
            justification=Gtk.Justification.LEFT, left_margin=6)
        self.box_container.pack_start(self.text_view_value, True, True, 0)
        self.text_buffer_value = self.text_view_value.get_buffer()

        # Text
        created = _('Created by')
        translated = _('Translated by')
        self.text_buffer_label.set_text(
            '{}\n'
            '{}'.format(created, translated)
            )
        self.text_buffer_value.set_text(
            'Alisson W.A.Gomes\n'
            'Alisson W.A.Gomes'
        )

        # CSS
        self.text_view_label.set_name('text-view-label')
        self.text_view_value.set_name('text-view-value')
        css = b'''
            #text-view-label{
                font-size: 12px;
                }
            #text-view-value{
                font-size: 12px;
                }
            '''
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
