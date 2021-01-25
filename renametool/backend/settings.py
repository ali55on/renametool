#!/usr/bin/env python3
import os
import logging
import json


class UserSettings(object):
    def __init__(self):
        self.__settings_path = os.getenv('HOME') + '/.config/rename_tool'
        self.__markup_settings_file = self.__settings_path + '/settings_markup.json'
        self.__colors_settings_file = self.__settings_path + '/settings_colors.json'
        self.__markup_settings = self.__load_markup_settings()
        self.__color_settings = self.__load_color_settings()

    def __markup_settings_already_exist(self) -> bool:
        try:
            os.makedirs(name=self.__settings_path, exist_ok=False)
            with open(self.__markup_settings_file, 'r') as m:
                m.read()
        except Exception as error:
            logging.info(error)
            already_exist = False
        else:
            already_exist = True

        return already_exist

    def __color_settings_already_exist(self) -> bool:
        try:
            os.makedirs(name=self.__settings_path, exist_ok=False)
            with open(self.__colors_settings_file, 'r') as c:
                c.read()
        except Exception as error:
            logging.info(error)
            already_exist = False
        else:
            already_exist = True

        return already_exist

    def __load_markup_settings(self) -> dict:
        if not self.__markup_settings_already_exist():
            self.__create_markup_settings()

        m = open(self.__markup_settings_file, 'r')
        data_markup = json.load(m)

        return data_markup

    def __load_color_settings(self) -> dict:
        if not self.__color_settings_already_exist():
            self.__create_color_settings()

        c = open(self.__colors_settings_file, 'r')
        data_color = json.load(c)

        return data_color

    def __create_markup_settings(self, settings: dict = None):
        if settings:
            markup_settings = settings
        else:
            markup_settings = {
                '[1, 2, 3]': '[1, 2, 3]',
                '[01, 02, 03]': '[01, 02, 03]',
                '[001, 002, 003]': '[001, 002, 003]',
                '[original-name]': '[Original filename]'
            }
        os.makedirs(name=self.__settings_path, exist_ok=True)
        with open(self.__markup_settings_file, 'w') as fp:
            json.dump(markup_settings, fp)

    def __create_color_settings(self, settings: dict = None):
        if settings:
            color_settings = settings
        else:
            color_settings = {
                'error-color': '#c33348',
                'warning-color': '#b8b445',
                'old-matching-color': '#d5440066',
                'new-matching-color': '#3b731e66',
                'extension-color': '#888888'
            }
        os.makedirs(name=self.__settings_path, exist_ok=True)
        with open(self.__colors_settings_file, 'w') as fp:
            json.dump(color_settings, fp)

    def get_markup_settings(self):
        """"""
        return self.__markup_settings

    def get_color_settings(self):
        """"""
        return self.__color_settings

    def set_markup_settings(self, settings: dict):
        """"""
        self.__create_markup_settings(settings=settings)

    def set_color_settings(self, settings: dict):
        """"""
        self.__create_color_settings(settings=settings)


if __name__ == '__main__':
    sett = UserSettings()
    mark = sett.get_markup_settings()
    color = sett.get_color_settings()

    for k, v in mark.items():
        print(k, '->', v)

    for k, v in color.items():
        print(k, '->', v)
