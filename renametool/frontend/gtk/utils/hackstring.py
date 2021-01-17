class SameSizeString(object):
    def __init__(self, first_str: str, last_str: str):
        self.first_str = first_str
        self.last_str = last_str

        self.__resolve()

    def __resolve(self):
        n_first_str = len(self.first_str)
        n_last_str = len(self.last_str)

        if n_first_str > n_last_str:
            dif = n_first_str - n_last_str
            div = int(dif / 2)
            self.last_str = (' ' * div) + self.last_str + (' ' * div)
        elif n_last_str > n_first_str:
            dif = n_last_str - n_first_str
            div = int(dif / 2)
            self.first_str = (' ' * div) + self.first_str + (' ' * div)

    def get_first_str(self):
        return self.first_str

    def get_last_str(self):
        return self.last_str


if __name__ == '__main__':
    ss = SameSizeString(first_str='O Rato', last_str='Roeu')
    print('***' + ss.get_first_str() + '***')
    print('***' + ss.get_last_str() + '***')
