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
        return self.text.replace(self.regex_match, self.markup_start + self.regex_match + self.markup_end)

    def mark_sub(self) -> str:
        return re.sub(self.regex_match, self.markup_start + self.regex_sub + self.markup_end, self.text)


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
