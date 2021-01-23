#!/usr/bin/env python3
import os

import backend.utils.file as file


markup_template = {
    '[1, 2, 3]': '[1, 2, 3]',
    '[01, 02, 03]': '[01, 02, 03]',
    '[001, 002, 003]': '[001, 002, 003]',
    '[original-name]': '[Original filename]'
}


class Rename(object):
    def __init__(self, list_files: list, new_name: str):
        self.__list_files = list_files
        self.__new_name = new_name

        self.__resume_error = None
        self.__resume_warning = None

        self.__rename_file_in_the_list()

    def get_resume_error(self):
        return self.__resume_error

    def get_resume_warning(self):
        return self.__resume_warning

    def __rename_file_in_the_list(self):
        list_markup_nums = self.__generate_markup_numbers()

        # Renomear arquivos
        all_names = list()
        for item_file, item_markup_num in zip(self.__list_files, list_markup_nums):
            new_name = self.__new_name.replace(markup_template['[1, 2, 3]'], item_markup_num)
            new_name = new_name.replace(markup_template['[01, 02, 03]'], item_markup_num)
            new_name = new_name.replace(markup_template['[001, 002, 003]'], item_markup_num)
            new_name = new_name.replace(markup_template['[original-name]'], item_file.get_original_name())
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

    def __generate_markup_numbers(self):
        num_items = len(self.__list_files) + 1
        if markup_template['[1, 2, 3]'] in self.__new_name:
            nums = list(str(x) for x in range(1, num_items))
        elif markup_template['[01, 02, 03]'] in self.__new_name:
            nums = list()
            for n in range(1, num_items):
                if n < 10:
                    nums.append('0' + str(n))
                else:
                    nums.append(str(n))
        elif markup_template['[001, 002, 003]'] in self.__new_name:
            nums = list()
            for n in range(1, num_items):
                if n < 10:
                    nums.append('00' + str(n))
                elif n < 100:
                    nums.append('0' + str(n))
                else:
                    nums.append(str(n))
        else:
            # noinspection PyUnusedLocal
            nums = list('' for x in range(1, num_items))

        return nums


if __name__ == '__main__':
    import os
    pt = os.path.dirname(os.path.abspath(__file__))
    ls = list(pt + '/' + x for x in os.listdir(pt))

    l_files = list()
    for url in ls:
        l_files.append(file.File(file_url=url))

    # Rename
    rename_status = Rename(
        list_files=l_files, new_name='.Gambá [original-name] [1, 2, 3]')

    if rename_status.get_resume_error():
        print('ERROR:', rename_status.get_resume_error())
    if rename_status.get_resume_warning():
        print('WARNING:', rename_status.get_resume_warning())

    for i in l_files:
        print(i.get_original_name() + i.get_extension() + ' -> ' + i.get_name() + i.get_extension())

    print(len(l_files))
