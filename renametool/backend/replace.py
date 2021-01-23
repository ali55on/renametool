#!/usr/bin/env python3
import os
import re

import backend.utils.file as file


class Replace(object):
    def __init__(self, list_files: list, search_text: str, replace_text: str):
        self.__list_files = list_files
        self.__search_text = search_text
        self.__replace_text = replace_text

        self.__resume_error = None
        self.__resume_warning = None

        self.__rename_file_in_the_list()

    def get_resume_error(self):
        return self.__resume_error

    def get_resume_warning(self):
        return self.__resume_warning

    def get_invalid_file(self):
        return self.__invalid_file

    def __rename_file_in_the_list(self):
        all_names = list()
        for item_file in self.__list_files:
            new_name = item_file.get_original_name().replace(self.__search_text, self.__replace_text)
            item_file.set_name(new_name)

            # Validar
            path = item_file.get_path()
            extension = item_file.get_extension()
            item_file.set_note(None)

            if not self.__resume_error:
                if new_name + extension in all_names:
                    # 'Filename already exists in the list'
                    self.__resume_error = 'repeated-name-error'
                    item_file.set_note('error')
                elif '/' in new_name:
                    # 'Names cannot contain the / (slash) character'
                    self.__resume_error = 'character-error'
                    item_file.set_note('error')
                elif new_name + extension == '.' or new_name + extension == '..':
                    # 'It is not possible to use one dot (.) or two dots (..) as a filename'
                    self.__resume_error = 'name-not-allowed-error'
                    item_file.set_note('error')
                elif new_name + extension in os.listdir(path):
                    # 'A file with that name already exists in the directory'
                    if new_name + extension != item_file.get_original_name() + extension:
                        self.__resume_error = 'existing-name-error'
                        item_file.set_note('error')
                elif len(new_name + extension) > 255:
                    # 'Filename longer than 255 characters (including extension)'
                    self.__resume_error = 'length-error'
                    item_file.set_note('error')

            if not self.__resume_warning:
                if new_name + extension != '.' and new_name + extension != '..':
                    if (new_name + extension)[0] == '.':
                        # 'Files that start with a dot (.) will be hidden'
                        self.__resume_warning = 'hidden-file-error'
                        item_file.set_note('warning')

            # Registrar para comparar nome repetido
            all_names.append(new_name + item_file.get_extension())


if __name__ == '__main__':
    import os

    pt = os.path.dirname(os.path.abspath(__file__))
    ls = list(pt + '/' + x for x in os.listdir(pt))

    l_files = list()
    for url in ls:
        l_files.append(file.File(file_url=url))

    # Replace
    replace_status = Replace(list_files=l_files, search_text='re', replace_text='RE')

    if replace_status.get_resume_error():
        print('ERROR:', replace_status.get_resume_error())
    if replace_status.get_resume_warning():
        print('WARNING:', replace_status.get_resume_warning())

    for i in l_files:
        print(i.get_original_name() + i.get_extension() + ' -> ' + i.get_name() + i.get_extension())

    print(len(l_files))
