from collections import namedtuple
from copy import copy

Year = namedtuple('Year', ['x'])
Month = namedtuple('Month', ['x'])
Week = namedtuple('Week', ['x'])
Day = namedtuple('Day', ['x'])
Daypart = namedtuple('Daypart', ['x'])
Hour = namedtuple('Hour', ['x'])
Minute = namedtuple('Minute', ['x'])
Second = namedtuple('Second', ['x'])

Interval = namedtuple('Interval', ['x', 'y'])


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


def word_to_num(s: str):

    for w in s.split():
        if w.isdigit():
            return int(w)

    _s = copy(s)
    res = {'dec': None, 'num': None}
    missing = 0

    decs = [('tizen', 'tiz'),
            ('huszon', 'husz'),
            'harminc',
            'negyven',
            'otven',
            'hatvan',
            'hetven',
            'nyolcvan',
            'kilencven']

    nums = ['nulla', 'egy', 'ketto', 'harom', 'negy', 'ot', 'hat', 'het', 'nyolc', 'kilenc']

    for i, dec in enumerate(decs):
        if type(dec) == tuple:
            for syn in dec:
                if syn in remove_accent(_s):
                    res['dec'] = (i+1) * 10
                    _s = _s[len(syn):]
                    break
        else:
            if dec in remove_accent(_s):
                res['dec'] = (i + 1) * 10
                _s = _s[len(syn):]
                break

    if not res['dec']:
        missing += 1
        res['dec'] = 0

    for i, num in enumerate(nums):
        if num in remove_accent(_s):
            res['num'] = i

    if res['num'] is None:
        missing += 1
        res['num'] = 0

    if missing < 2:
        return res['dec'] + res['num']
    else:
        return -1
