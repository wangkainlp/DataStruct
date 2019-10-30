#coding:utf-8

def unicode_to_utf8(ch):

    if 0x00000000 <= ch and ch <= 0x0000007F:
        pass
    elif 0x00000080 <= ch and ch <= 0x000007FF:
        pass
    elif 0x00000800 <= ch and ch <= 0x0000FFFF:
        pass
    elif 0x00010000 <= ch and ch <= 0x001FFFFF:
        pass
    elif 0x00200000 <= ch and ch <= 0x03FFFFFF:
        pass
    elif 0x04000000 <= ch and ch <= 0x7FFFFFFF:
        pass


def utf8_to_unicode(ch):
    pass

if __name__ == '__main__':
    print ''

