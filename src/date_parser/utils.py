from collections import namedtuple


Year = namedtuple('Year', ['x'])
Month = namedtuple('Month', ['x'])
Week = namedtuple('Week', ['x'])
Day = namedtuple('Day', ['x'])
Hour = namedtuple('Hour', ['x'])
Minute = namedtuple('Minute', ['x'])
Second = namedtuple('Second', ['x'])


def remove_accent(s: str):
    mapping = {'á': 'a',
               'é': 'e',
               'í': 'i',
               'ó': 'o',
               'ú': 'u',
               'ö': 'o',
               'ü': 'u',
               'ő': 'o',
               'ű': 'u'}

    for a, b in mapping.items():
        s = s.replace(a, b)

    return s
