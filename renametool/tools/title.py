#!/usr/bin/env python3
import os


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

        if self.__have_dirs and self.__have_files:
            return 'Rename {} files and folders'.format(str(len(self.__file_list)))
        elif self.__have_dirs and not self.__have_files:
            return 'Rename {} folders'.format(str(len(self.__file_list)))
        elif not self.__have_dirs and self.__have_files:
            return 'Rename {} files'.format(str(len(self.__file_list)))
