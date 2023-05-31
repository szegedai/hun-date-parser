import re
from typing import Dict, List, Any
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from .patterns import (R_ISO_DATE, R_NAMED_MONTH, R_TODAY, R_TOMORROW, R_NTOMORROW, R_YESTERDAY, R_NYESTERDAY,
                       R_WEEKDAY, R_WEEK, R_YEAR, R_NDAYS_FROM_NOW, R_NWEEKS_FROM_NOW, R_NHOURS_FROM_NOW,
                       R_NMINS_FROM_NOW, R_RELATIVE_MONTH, R_NMINS_PRIOR_NOW, R_NDAYS_PRIOR_NOW, R_NHOURS_PRIOR_NOW,
                       R_NWEEKS_PRIOR_NOW, R_IN_PAST_PERIOD_MINS, R_IN_PAST_PERIOD_HOURS, R_IN_PAST_PERIOD_DAYS,
                       R_IN_PAST_PERIOD_WEEKS, R_IN_PAST_PERIOD_MONTHS, R_IN_PAST_PERIOD_YEARS)
from hun_date_parser.utils import remove_accent, word_to_num, Year, Month, Week, Day, Hour, Minute, OverrideTopWithNow


def match_iso_date(s: str) -> List[Dict[str, Any]]:
    """
    Match ISO date-like format.
    :param s: textual input
    :return: tuple of date parts
    """
    match = re.findall(R_ISO_DATE, s)

    res = []
    if match:
        for group in match:
            group = [int(m.lstrip('0')) for m in group if m.lstrip('0')]

            if len(group) == 1:
                res.append({'match': group, 'date_parts': [Year(group[0], 'match_iso_date')]})
            elif len(group) == 2:
                res.append({'match': group,
                            'date_parts': [Year(group[0], 'match_iso_date'), Month(group[1], 'match_iso_date')]})
            elif len(group) == 3:
                res.append({'match': group,
                            'date_parts': [Year(group[0], 'match_iso_date'), Month(group[1], 'match_iso_date'),
                                           Day(group[2], 'match_iso_date')]})

    return res


def match_named_month(s: str, now: datetime) -> List[Dict[str, Any]]:
    """
    Match named month and day
    :param s: textual input
    :return: tuple of date parts
    """
    groups = re.findall(R_NAMED_MONTH, s)
    months = ['jan', 'feb', 'mar', 'apr', 'maj', 'jun', 'jul', 'aug', 'szep', 'okt', 'nov', 'dec']

    res = []
    groups = [(mod, m, d.lstrip('0')) if d else (mod, m, '') for mod, m, d in groups]
    for group in groups:
        group_res = {'match': group, 'date_parts': []}
        if group[0]:
            if 'jovo' in remove_accent(group[0]):
                group_res['date_parts'].append(Year(now.year + 1, 'named_month'))
            elif 'tavaly' in remove_accent(group[0]):
                group_res['date_parts'].append(Year(now.year - 1, 'named_month'))

        for i, month in enumerate(months):
            if month in remove_accent(group[1]):
                group_res['date_parts'].append(Month(i + 1, 'named_month'))
                break

        if group[2]:
            group_res['date_parts'].append(Day(int(group[2]), 'named_month'))

        res.append(group_res)

    return res


def match_relative_day(s: str, now: datetime) -> List[Dict[str, Any]]:
    groups = [*re.findall(R_TODAY, s),
              *re.findall(R_TOMORROW, s),
              *re.findall(R_NTOMORROW, s),
              *re.findall(R_YESTERDAY, s),
              *re.findall(R_NYESTERDAY, s)]

    res = []
    for group in groups:

        if type(group) != str:
            group = [m for m in group if m][0]

        if 'ma' in group or 'má' in group:
            res.append({'match': group, 'date_parts': [Year(now.year, 'relative_day'), Month(now.month, 'relative_day'),
                                                       Day(now.day, 'relative_day')]})
        elif 'holnapu' in group:
            tom2 = now + timedelta(days=2)
            res.append({'match': group,
                        'date_parts': [Year(tom2.year, 'relative_day'), Month(tom2.month, 'relative_day'),
                                       Day(tom2.day, 'relative_day')]})
        elif 'holnap' in group:
            tom = now + timedelta(days=1)
            res.append({'match': group, 'date_parts': [Year(tom.year, 'relative_day'), Month(tom.month, 'relative_day'),
                                                       Day(tom.day, 'relative_day')]})
        elif 'tegnapel' in group:
            yes2 = now - timedelta(days=2)
            res.append({'match': group,
                        'date_parts': [Year(yes2.year, 'relative_day'), Month(yes2.month, 'relative_day'),
                                       Day(yes2.day, 'relative_day')]})
        elif 'tegnap' in group:
            yes = now - timedelta(days=1)
            res.append({'match': group, 'date_parts': [Year(yes.year, 'relative_day'), Month(yes.month, 'relative_day'),
                                                       Day(yes.day, 'relative_day')]})

    return res


def match_weekday(s: str, now: datetime, expect_future_day: bool = False) -> List[Dict[str, Any]]:
    groups = re.findall(R_WEEKDAY, s)

    res = []
    for group in groups:
        date_parts = {'match': group, 'date_parts': []}
        week, day = group
        n_weeks = 0

        if 'jovo' in remove_accent(week):
            n_weeks = 1
        elif 'mult' in remove_accent(week) or 'elozo' in remove_accent(week):
            n_weeks = -1

        def offset_date(date):
            if date.strftime("%Y-%m-%d") < now.strftime("%Y-%m-%d"):
                return date + timedelta(days=7)
            return date

        def get_day_of_week(w, d):
            return ((now - timedelta(days=now.weekday())) + timedelta(days=w * 7)) + timedelta(days=d)

        if 'hetfo' in remove_accent(day):
            day = offset_date(get_day_of_week(n_weeks, 0)) if expect_future_day and n_weeks >= 0 \
                else get_day_of_week(n_weeks, 0)
            date_parts['date_parts'] = [Year(day.year, 'weekday'), Month(day.month, 'weekday'), Day(day.day, 'weekday')]
        elif 'kedd' in remove_accent(day):
            day = offset_date(get_day_of_week(n_weeks, 1)) if expect_future_day and n_weeks >= 0 \
                else get_day_of_week(n_weeks, 1)
            date_parts['date_parts'] = [Year(day.year, 'weekday'), Month(day.month, 'weekday'), Day(day.day, 'weekday')]
        elif 'szerda' in remove_accent(day):
            day = offset_date(get_day_of_week(n_weeks, 2)) if expect_future_day and n_weeks >= 0 \
                else get_day_of_week(n_weeks, 2)
            date_parts['date_parts'] = [Year(day.year, 'weekday'), Month(day.month, 'weekday'), Day(day.day, 'weekday')]
        elif 'csut' in remove_accent(day):
            day = offset_date(get_day_of_week(n_weeks, 3)) if expect_future_day and n_weeks >= 0 \
                else get_day_of_week(n_weeks, 3)
            date_parts['date_parts'] = [Year(day.year, 'weekday'), Month(day.month, 'weekday'), Day(day.day, 'weekday')]
        elif 'pent' in remove_accent(day):
            day = offset_date(get_day_of_week(n_weeks, 4)) if expect_future_day and n_weeks >= 0 \
                else get_day_of_week(n_weeks, 4)
            date_parts['date_parts'] = [Year(day.year, 'weekday'), Month(day.month, 'weekday'), Day(day.day, 'weekday')]
        elif 'szom' in remove_accent(day):
            day = offset_date(get_day_of_week(n_weeks, 5)) if expect_future_day and n_weeks >= 0 \
                else get_day_of_week(n_weeks, 5)
            date_parts['date_parts'] = [Year(day.year, 'weekday'), Month(day.month, 'weekday'), Day(day.day, 'weekday')]
        elif 'vas' in remove_accent(day):
            day = offset_date(get_day_of_week(n_weeks, 6)) if expect_future_day and n_weeks >= 0 \
                else get_day_of_week(n_weeks, 6)
            date_parts['date_parts'] = [Year(day.year, 'weekday'), Month(day.month, 'weekday'), Day(day.day, 'weekday')]

        res.append(date_parts)

    return res


def match_week(s: str, now: datetime) -> List[Dict[str, Any]]:
    groups = re.findall(R_WEEK, s)

    res = []
    for group in groups:
        date_parts = {'match': group, 'date_parts': []}

        if 'ez' in group:
            y, w = now.isocalendar()[0:2]
            date_parts['date_parts'].extend([Year(y, 'week'), Week(w, 'week')])
        elif 'jovo' in remove_accent(group):
            y, w = (now + timedelta(days=7)).isocalendar()[0:2]
            date_parts['date_parts'].extend([Year(y, 'week'), Week(w, 'week')])
        elif 'mult' in remove_accent(group) or 'elozo' in remove_accent(group):
            y, w = (now - timedelta(days=7)).isocalendar()[0:2]
            date_parts['date_parts'].extend([Year(y, 'week'), Week(w, 'week')])

        res.append(date_parts)

    return res


def match_n_periods_compared_to_now(s: str, now: datetime) -> List[Dict[str, Any]]:
    fn = 'n_date_periods_compared_to_now'

    regexes = [
        (R_NWEEKS_FROM_NOW, 'w', 'future'),
        (R_NDAYS_FROM_NOW, 'd', 'future'),
        (R_NHOURS_FROM_NOW, 'h', 'future'),
        (R_NMINS_FROM_NOW, 'm', 'future'),
        (R_NWEEKS_PRIOR_NOW, 'w', 'past'),
        (R_NDAYS_PRIOR_NOW, 'd', 'past'),
        (R_NHOURS_PRIOR_NOW, 'h', 'past'),
        (R_NMINS_PRIOR_NOW, 'm', 'past'),
    ]
    res = []

    for regex, freq, before_or_after in regexes:
        multiplier = -1 if before_or_after == "past" else 1
        groups = re.findall(regex, s)
        for group in groups:
            date_parts = {'match': group, 'date_parts': []}

            n = group[1]
            if n:
                n = word_to_num(n)

                if n == -1:
                    continue

                if freq == 'w':
                    res_dt = (now + timedelta(days=multiplier * 7 * n))
                    y, m, d = res_dt.year, res_dt.month, res_dt.day
                    date_parts['date_parts'].extend([Year(y, fn), Month(m, fn), Day(d, fn)])
                elif freq == 'd':
                    res_dt = (now + timedelta(days=multiplier * n))
                    y, m, d = res_dt.year, res_dt.month, res_dt.day
                    date_parts['date_parts'].extend([Year(y, fn), Month(m, fn), Day(d, fn)])
                elif freq == 'h':
                    res_dt = (now + timedelta(hours=multiplier * n))
                    y, m, d, h = res_dt.year, res_dt.month, res_dt.day, res_dt.hour
                    date_parts['date_parts'].extend([Year(y, fn), Month(m, fn), Day(d, fn), Hour(h, fn)])
                elif freq == 'm':
                    res_dt = (now + timedelta(minutes=multiplier * n))
                    y, mo, d, h, mi = res_dt.year, res_dt.month, res_dt.day, res_dt.hour, res_dt.minute
                    date_parts['date_parts'].extend([Year(y, fn), Month(mo, fn),
                                                     Day(d, fn), Hour(h, fn), Minute(mi, fn)])

            res.append(date_parts)

    return res


def match_named_year(s: str, now: datetime) -> List[Dict[str, Any]]:
    groups = re.findall(R_YEAR, s)

    res = []
    for group in groups:
        date_parts = {'match': group, 'date_parts': []}

        if 'tavalyelott' in remove_accent(group):
            date_parts['date_parts'] = [Year(now.year - 2, 'named_year')]
        elif 'tavaly' in remove_accent(group):
            date_parts['date_parts'] = [Year(now.year - 1, 'named_year')]
        elif 'iden' in remove_accent(group):
            date_parts['date_parts'] = [Year(now.year, 'named_year')]
        elif 'jovo' in remove_accent(group):
            date_parts['date_parts'] = [Year(now.year + 1, 'named_year')]
        elif 'mulva' in remove_accent(group):
            num_after = word_to_num(group)

            if num_after == -1:
                continue

            if num_after != -1:
                date_parts['date_parts'] = [Year(now.year + num_after, 'named_year')]
        elif 'ezelott' in remove_accent(group) or 'korabban' in remove_accent(group):
            num_before = word_to_num(group)

            if num_before == -1:
                continue

            if num_before != -1:
                date_parts['date_parts'] = [Year(now.year - num_before, 'named_year')]

        res.append(date_parts)

    return res


def match_relative_month(s: str, now: datetime) -> List[Dict[str, Any]]:
    groups = re.findall(R_RELATIVE_MONTH, s)

    res = []
    for group in groups:
        date_parts = {'match': group, 'date_parts': []}

        if ('mult' in remove_accent(group)
                or 'elozo' in remove_accent(group)
                or 'utolso' in remove_accent(group)
                or 'utobbi' in remove_accent(group)):
            prev_month = now.date() + relativedelta(months=-1)
            date_parts['date_parts'] = [Year(prev_month.year, 'relative_month'),
                                        Month(prev_month.month, 'relative_month')]
        elif (remove_accent(group).startswith("ezen")
                or 'ebben' in remove_accent(group)
                or 'aktualis' in remove_accent(group)):
            date_parts['date_parts'] = [Year(now.year, 'relative_month'), Month(now.month, 'relative_month')]
        elif ('jovo' in remove_accent(group)
                or 'kovetkez' in remove_accent(group)):
            next_month = now.date() + relativedelta(months=1)
            date_parts['date_parts'] = [Year(next_month.year, 'relative_month'),
                                        Month(next_month.month, 'relative_month')]

        res.append(date_parts)

    return res


def match_in_past_n_periods(s: str, now: datetime) -> List[Dict[str, Any]]:
    fn = 'in_past_n_periods'

    regexes = [
        (R_IN_PAST_PERIOD_YEARS, 'year', 'past'),
        (R_IN_PAST_PERIOD_MONTHS, 'month', 'past'),
        (R_IN_PAST_PERIOD_WEEKS, 'week', 'past'),
        (R_IN_PAST_PERIOD_DAYS, 'day', 'past'),
        (R_IN_PAST_PERIOD_HOURS, 'hour', 'past'),
        (R_IN_PAST_PERIOD_MINS, 'minute', 'past'),
    ]
    res = []

    for regex, freq, before_or_after in regexes:
        multiplier = -1 if before_or_after == "past" else 1
        groups = re.findall(regex, s)
        for group in groups:
            date_parts = {'match': group, 'date_parts': []}

            n = group[1]
            if n:
                n = word_to_num(n) if n != " " else 1

                if n == -1:
                    continue

                if freq == 'year':
                    res_dt = (now + relativedelta(years=multiplier * n))
                    y, m, d = res_dt.year, res_dt.month, res_dt.day
                    date_parts['date_parts'].extend([Year(y, fn), Month(m, fn), Day(d, fn),
                                                     OverrideTopWithNow(None, fn)])

                elif freq == 'month':
                    res_dt = now + relativedelta(months=multiplier * n)
                    y, m, d = res_dt.year, res_dt.month, res_dt.day
                    date_parts['date_parts'].extend([Year(y, fn), Month(m, fn), Day(d, fn),
                                                     OverrideTopWithNow(None, fn)])

                elif freq == 'week':
                    res_dt = (now + timedelta(days=multiplier * 7 * n))
                    y, m, d = res_dt.year, res_dt.month, res_dt.day
                    date_parts['date_parts'].extend([Year(y, fn), Month(m, fn), Day(d, fn),
                                                     OverrideTopWithNow(None, fn)])
                elif freq == 'day':
                    res_dt = (now + timedelta(days=multiplier * n))
                    y, m, d = res_dt.year, res_dt.month, res_dt.day
                    date_parts['date_parts'].extend([Year(y, fn), Month(m, fn), Day(d, fn),
                                                     OverrideTopWithNow(None, fn)])
                elif freq == 'hour':
                    res_dt = (now + timedelta(hours=multiplier * n))
                    y, m, d, h = res_dt.year, res_dt.month, res_dt.day, res_dt.hour
                    date_parts['date_parts'].extend([Year(y, fn), Month(m, fn), Day(d, fn), Hour(h, fn),
                                                     OverrideTopWithNow(None, fn)])
                elif freq == 'minute':
                    res_dt = (now + timedelta(minutes=multiplier * n))
                    y, mo, d, h, mi = res_dt.year, res_dt.month, res_dt.day, res_dt.hour, res_dt.minute
                    date_parts['date_parts'].extend([Year(y, fn), Month(mo, fn),
                                                     Day(d, fn), Hour(h, fn), Minute(mi, fn),
                                                     OverrideTopWithNow(None, fn)])

            res.append(date_parts)

    return res
