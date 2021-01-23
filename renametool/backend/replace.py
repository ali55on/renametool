#!/usr/bin/env python3
import os
import re

import backend.utils.file as file


class Replace(object):
    def __init__(self, list_files: list, search_text: str, replace_text: str):
        self.__list_files = list_files
        self.__search_text = search_text
        self.__replace_text = replace_text

        self.__error_found = None

        self.__rename_file_in_the_list()

    def get_error_found(self):
        return self.__error_found

    def get_invalid_file(self):
        return self.__invalid_file

    def __rename_file_in_the_list(self):
        all_names = list()
        errors_found = {
            'repeated-name-error': False,
            'character-error': False,
            'name-not-allowed-error': False,
            'existing-name-error': False,
            'length-error': False,
            'hidden-file-error': False
        }
        for item_file in self.__list_files:
            path = item_file.get_path()
            extension = item_file.get_extension()
            item_file.set_note(None)

            new_name = item_file.get_original_name().replace(self.__search_text, self.__replace_text)
            item_file.set_name(new_name)

            # Completely unnamed
            if new_name + extension == '':
                item_file.set_note('completely-unnamed')
                errors_found['completely-unnamed'] = True

            # 'Filename already exists in the list'
            elif new_name + extension in all_names:
                item_file.set_note('repeated-name-error')
                errors_found['repeated-name-error'] = True

            # 'Names cannot contain the / (slash) character'
            elif '/' in new_name:
                item_file.set_note('character-error')
                errors_found['character-error'] = True

            # 'It is not possible to use one dot (.) or two dots (..) as a filename'
            elif new_name + extension == '.' or new_name + extension == '..':
                item_file.set_note('name-not-allowed-error')
                errors_found['name-not-allowed-error'] = True

            # 'A file with that name already exists in the directory'
            elif new_name + extension in os.listdir(path):
                if new_name + extension != item_file.get_original_name() + extension:
                    item_file.set_note('existing-name-error')
                    errors_found['existing-name-error'] = True

            # 'Filename longer than 255 characters (including extension)'
            elif len(new_name + extension) > 255:
                item_file.set_note('length-error')
                errors_found['length-error'] = True

            # 'Files that start with a dot (.) will be hidden'
            elif new_name + extension != '.' and new_name + extension != '..':
                if new_name + extension and (new_name + extension)[0] == '.':
                    item_file.set_note('hidden-file-error')
                    errors_found['hidden-file-error'] = True

            # Registrar para comparar nome repetido
            all_names.append(new_name + item_file.get_extension())

        # Highest level error
        errors_list = [
            'completely-unnamed', 'repeated-name-error', 'character-error',
            'name-not-allowed-error', 'existing-name-error', 'length-error',
            'hidden-file-error']

        for error in errors_list:
            if error in errors_found and errors_found[error]:
                self.__error_found = error
                break


if __name__ == '__main__':
    import os

    pt = os.path.dirname(os.path.abspath(__file__))
    ls = list(pt + '/' + x for x in os.listdir(pt))

    l_files = list()
    for url in ls:
        l_files.append(file.File(file_url=url))

    # Replace
    replace_status = Replace(list_files=l_files, search_text='re', replace_text='RE')

    if replace_status.get_error_found():
        print('ERROR:', replace_status.get_error_found())
    if replace_status.get_resume_warning():
        print('WARNING:', replace_status.get_resume_warning())

    for i in l_files:
        print(i.get_original_name() + i.get_extension() + ' -> ' + i.get_name() + i.get_extension())

    print(len(l_files))
