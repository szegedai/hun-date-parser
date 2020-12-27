from datetime import date

days = [
    ['hétfő', 'hétfőn'],
    ['kedd', 'kedden'],
    ['szerda', 'szerdán'],
    ['csütörtök', 'csütörtökön'],
    ['péntek', 'pénteken'],
    ['szombat', 'szombaton'],
    ['vasárnap']
]

months = [
    'január',
    'február',
    'március',
    'április',
    'május',
    'június',
    'július',
    'augusztus',
    'szeptember',
    'október',
    'november',
    'december'
]


def is_day_of(d):
    return days[d.weekday()][-1]


def date2text(d: date, now: date):
    resp = ''
    day_diff = (d - now).days
    till_next_week = 7 - now.weekday() - 1
    till_last_week = -1 * now.weekday()

    if till_last_week - 14 < day_diff <= till_last_week - 7:
        resp += 'két hete ' + is_day_of(d)
    elif till_last_week - 7 < day_diff < till_last_week:
        resp += 'múlt héten ' + is_day_of(d)
    elif day_diff == 0:
        resp += 'ma'
    elif day_diff == 1:
        resp += 'holnap'
    elif till_last_week <= day_diff < till_next_week:
        resp += 'ezen a héten ' + is_day_of(d)
    elif till_next_week < day_diff <= till_next_week + 7:
        resp += 'jövő hét ' + is_day_of(d)
    elif till_next_week + 7 < day_diff <= till_next_week + 14:
        resp += 'két hét múlva ' + is_day_of(d)
    else:
        resp += f'{d.year}-{d.month}-{d.day}'

    return resp


def date2full_text(d: date):
    return f'{d.year} {months[d.month - 1]} {d.day}'
