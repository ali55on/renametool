#!/usr/bin/env python3
import os
import gettext
import locale

path = os.path.dirname(os.path.abspath(__file__))
path_locales = path.replace('tools', 'locales')
current_locale, encoding = locale.getdefaultlocale()

t = gettext.translation('title', path_locales, [current_locale])
_ = t.gettext

gettext.install('title')


class Title(object):
    def __init__(self, file_list: list):
        # Args
        self.__file_list = file_list

        # Flags
        self.__have_dirs = False
        self.__have_files = False

        # Title
        self.__title = self.__set_title()

    def get_title(self):
        """"""
        return self.__title

    def __set_title(self):
        for file in self.__file_list:
            if os.path.isdir(file.get_url()):
                self.__have_dirs = True
            else:
                self.__have_files = True

        itens_num = len(self.__file_list)
        rename_prefix = '{} {} '.format(_('Rename'), str(itens_num))

        if self.__have_dirs and self.__have_files:
            return rename_prefix +_('files and folders')

        elif self.__have_dirs and not self.__have_files:
            if itens_num == 1:
                return rename_prefix + _('folder')
            return rename_prefix + _('folders')

        elif not self.__have_dirs and self.__have_files:
            if itens_num == 1:
                return rename_prefix + _('file')
            return rename_prefix + _('files')
