#!/usr/bin/env python3
import re


class MarkMatchText(object):
    def __init__(self, text: str, regex_match: str, regex_sub: str, markup_start: str = '<', markup_end: str = '>'):
        self.text = text
        self.regex_match = regex_match
        self.regex_sub = regex_sub
        self.markup_start = markup_start
        self.markup_end = markup_end

    def mark_match(self) -> str:
        try:
            re_search = re.search(self.regex_match, self.text)
            if re_search:
                find = re_search.group(0)
                if find in self.text:
                    txt = re.sub(find, self.markup_start + find + self.markup_end, self.text)
                else:
                    txt = self.text
            else:
                txt = self.text

        except Exception as error:
            print(error)
            txt = self.regex_match

        return txt

    def mark_sub(self) -> str:
        try:
            txt = re.sub(self.regex_match, self.markup_start + self.regex_sub + self.markup_end, self.text)
        except Exception as error:
            print(error)
            txt = self.regex_match

        return txt


if __name__ == '__main__':
    m = MarkMatchText(
        text='O rato roeu a roupa do rei de roma 1. A roupa ficou esburacada',
        regex_match='roupa', regex_sub='perna'
    )
    print(m.mark_match())
    print(m.mark_sub())
    print('.......')
    m = MarkMatchText(
        text='O rato roeu a roupa do rei de roma 2. A roupa ficou esburacada',
        regex_match=r'\d..+', regex_sub='fim',
        markup_start='[', markup_end=']'
    )
    print(m.mark_match())
    print(m.mark_sub())
