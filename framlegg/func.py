# vim: ts=4 sts=4 expandtab sw=4 fileencoding=utf8
import re

def cmp_str_as_int(a, b):
    a = re.match(r'^[^\d]*(\d+)', a).group(1)
    b = re.match(r'^[^\d]*(\d+)', b).group(1)

    return cmp(int(a), int(b))
