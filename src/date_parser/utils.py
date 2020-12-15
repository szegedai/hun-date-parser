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

    _s = '<DEL>' + remove_accent(copy(s))
    res = {'dec': -1, 'num': -1}
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

    nums = ['nulla', 'egy', ('ketto', 'ket'), 'harom', 'negy', 'ot', 'hat', 'het', 'nyolc', 'kilenc']

    for i, dec in enumerate(decs):
        if type(dec) == tuple:
            for syn in dec:
                if syn in _s:
                    res['dec'] = (i+1) * 10
                    _s = _s.replace(syn, '<DEL>')
                    break
        else:
            if dec in _s:
                res['dec'] = (i + 1) * 10
                _s = _s.replace(dec, '<DEL>')
                break

    if res['dec'] == -1:
        missing += 1
        res['dec'] = 0

    for i, num in enumerate(nums):
        if type(num) == tuple:
            for num_syn in num:
                if '<DEL>' + num_syn in _s or ' ' + num_syn in _s:
                    res['num'] = i
        else:
            if '<DEL>' + str(num) in _s or ' ' + str(num) in _s:
                res['num'] = i

    if res['num'] == -1:
        missing += 1
        res['num'] = 0

    if missing < 2:
        return res['dec'] + res['num']
    else:
        return -1
