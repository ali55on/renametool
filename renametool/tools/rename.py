#!/usr/bin/env python3
import os

import tools.utils.file as file


class Rename(object):
    def __init__(self, markup_settings, list_files: list, new_name: str):
        # Args
        self.__list_files = list_files
        self.markup_settings = markup_settings
        self.__new_name = new_name

        # Flags
        self.__error_found = None

        # Sett
        self.__rename_file_in_the_list()

    def get_error_found(self):
        return self.__error_found

    def __rename_file_in_the_list(self):
        list_markup_nums = self.__generate_markup_numbers()

        # Renomear arquivos
        all_names = list()
        errors_found = dict()
        for item_file, item_markup_num in zip(self.__list_files, list_markup_nums):
            item_file.set_note(None)
            new_name = self.__new_name.replace(self.markup_settings['[1, 2, 3]'], item_markup_num)
            new_name = new_name.replace(self.markup_settings['[01, 02, 03]'], item_markup_num)
            new_name = new_name.replace(self.markup_settings['[001, 002, 003]'], item_markup_num)
            new_name = new_name.replace(self.markup_settings['[original-name]'], item_file.get_original_name())
            item_file.set_name(new_name)

            # Validar
            path = item_file.get_path()
            extension = item_file.get_extension()

            # 'Filename already exists in the list'
            if new_name + extension in all_names:
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
                if (new_name + extension)[0] == '.':
                    item_file.set_note('hidden-file-error')
                    errors_found['hidden-file-error'] = True

            # Registrar para comparar nome repetido
            all_names.append(new_name + item_file.get_extension())

        # Highest level error
        errors_list = [
            'repeated-name-error', 'character-error', 'name-not-allowed-error',
            'existing-name-error', 'length-error', 'hidden-file-error']

        for error in errors_list:
            if error in errors_found and errors_found[error]:
                self.__error_found = error
                break

    def __generate_markup_numbers(self):
        num_items = len(self.__list_files) + 1
        if self.markup_settings['[1, 2, 3]'] in self.__new_name:
            nums = list(str(x) for x in range(1, num_items))
        elif self.markup_settings['[01, 02, 03]'] in self.__new_name:
            nums = list()
            for n in range(1, num_items):
                if n < 10:
                    nums.append('0' + str(n))
                else:
                    nums.append(str(n))
        elif self.markup_settings['[001, 002, 003]'] in self.__new_name:
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
    markup_template = {
        '[1, 2, 3]': '[1, 2, 3]',
        '[01, 02, 03]': '[01, 02, 03]',
        '[001, 002, 003]': '[001, 002, 003]',
        '[original-name]': '[Original filename]'
    }
    rename_status = Rename(
        markup_settings=markup_template,
        list_files=l_files, new_name='.Gambá [original-name] [1, 2, 3]')

    if rename_status.get_error_found():
        print('ERROR:', rename_status.get_error_found())
    if rename_status.get_resume_warning():
        print('WARNING:', rename_status.get_resume_warning())

    for i in l_files:
        print(i.get_original_name() + i.get_extension() + ' -> ' + i.get_name() + i.get_extension())

    print(len(l_files))
