#!/usr/bin/env python3
import re

import utils.file as file
import utils.markmatchtext as mark_match_text


markup_start = '<<'
markup_end = '>>'


class ReplacePreview(object):
    def __init__(self, list_files: list, search_text: str, replace_text: str):
        self.__list_files = list_files
        self.__search_text = search_text
        self.__replace_text = replace_text

        self.__match_list = list()
        self.__replace_list = list()

        self.__generate_lists()

    def get_match_list(self):
        return self.__match_list

    def get_replace_list(self):
        return self.__replace_list

    def __generate_lists(self):
        for item in self.__list_files:
            text = item.get_original_name()
            ext = item.get_extension()

            match = mark_match_text.MarkMatchText(
                text=text,
                regex_match=self.__search_text, regex_sub=self.__replace_text,
                markup_start=markup_start, markup_end=markup_end)

            self.__match_list.append(match.mark_match() + ext)
            self.__replace_list.append(match.mark_sub() + ext)


if __name__ == '__main__':
    import os

    pt = os.path.dirname(os.path.abspath(__file__))
    ls = list(pt + '/' + x for x in os.listdir(pt))

    l_files = list()
    for url in ls:
        l_files.append(file.File(file_url=url))

    # Replace preview
    rp = ReplacePreview(list_files=l_files, search_text='re', replace_text='RE')
    list_match = rp.get_match_list()
    list_replace = rp.get_replace_list()
    for m, r in zip(list_match, list_replace):
        print(m + ' -> ' + r)
