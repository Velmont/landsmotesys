# vim: ts=4 sts=4 expandtab sw=4 fileencoding=utf8
import re

def cmp_str_as_int(a, b):
    a = re.match(r'^\d+', a).group(0)
    b = re.match(r'^\d+', b).group(0)

    return cmp(int(a), int(b))
