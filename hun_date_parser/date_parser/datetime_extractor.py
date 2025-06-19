"""This module handles combined date and time parsing."""

from datetime import datetime, timedelta, date, time
from calendar import monthrange
from itertools import chain

from typing import Dict, List, Union, Any
from copy import copy

from hun_date_parser.date_parser.structure_parsers import match_multi_match, match_interval, match_duration_match
from hun_date_parser.date_parser.date_parsers import (match_named_month, match_iso_date, match_weekday,
                                                      match_relative_day, match_day_of_month,
                                                      match_week, match_named_year, match_n_periods_compared_to_now,
                                                      match_relative_month, match_in_past_n_periods,
                                                      match_date_offset, match_named_month_interval,
                                                      match_named_month_start_mid_end)
from hun_date_parser.date_parser.time_parsers import match_digi_clock, match_time_words, match_now, match_hwords
from hun_date_parser.utils import (Year, Month, Week, Day, Daypart, Hour, Minute, StartDay, EndDay, get_type_if_exists,
                                   OverrideTopWithNow, SearchScopes, is_smaller_date_or_none,
                                   OverrideBottomWithNow, monday_of_calenderweek, DateTimePartConatiner,
                                   return_on_value_error, filter_offset_objects, apply_offsets_and_return_components)

datelike = Union[datetime, date, time, None]

daypart_mapping = [
    (3, 5),  # hajnal
    (6, 10),  # reggel
    (8, 11),  # délelőtt
    (12, 18),  # délután
    (18, 21),  # este
    (22, 2)  # éjjel
]


def text2datetime(input_sentence: str, now: datetime = datetime.now(),
                  search_scope: SearchScopes = SearchScopes.NOT_RESTRICTED,
                  realistic_year_required: bool = True, return_spans: bool = False) -> List[Dict[str, Any]]:
    """
    Returns the list of datetime intervals found in the input sentence.
    :param input_sentence: Input sentence string.
    :param now: Current timestamp to calculate relative dates.
    :param search_scope: Defines whether the timeframe should be restricted to past or future.
    :param realistic_year_required: Defines whether to restrict year candidates to be between 1900 and 2100.
    :param return_spans: Whether to include span information in the results.
    :return: list of datetime interval dictionaries
    """
    datetime_extractor = DatetimeExtractor(now=now,
                                           output_container='datetime',
                                           search_scope=search_scope,
                                           realistic_year_required=realistic_year_required,
                                           return_spans=return_spans)
    return datetime_extractor.parse_datetime(sentence=input_sentence)


def text2date(input_sentence: str, now: datetime = datetime.now(),
              search_scope: SearchScopes = SearchScopes.NOT_RESTRICTED,
              realistic_year_required: bool = True, return_spans: bool = False) -> List[Dict[str, Any]]:
    """
    Returns the list of date intervals found in the input sentence.
    :param input_sentence: Input sentence string.
    :param now: Current timestamp to calculate relative dates.
    :param search_scope: Defines whether the timeframe should be restricted to past or future.
    :param realistic_year_required: Defines whether to restrict year candidates to be between 1900 and 2100.
    :param return_spans: Whether to include span information in the results.
    :return: list of date interval dictionaries
    """
    datetime_extractor = DatetimeExtractor(now=now, output_container='date',
                                           search_scope=search_scope,
                                           realistic_year_required=realistic_year_required,
                                           return_spans=return_spans)
    return datetime_extractor.parse_datetime(sentence=input_sentence)


def text2time(input_sentence: str, now: datetime = datetime.now(),
              search_scope: SearchScopes = SearchScopes.NOT_RESTRICTED,
              realistic_year_required: bool = True, return_spans: bool = False) -> List[Dict[str, Any]]:
    """
    Returns the list of time intervals found in the input sentence.
    :param input_sentence: Input sentence string.
    :param now: Current timestamp to calculate relative dates.
    :param search_scope: Defines whether the timeframe should be restricted to past or future.
    :param realistic_year_required: Defines whether to restrict year candidates to be between 1900 and 2100.
    :param return_spans: Whether to include span information in the results.
    :return: list of time interval dictionaries
    """
    datetime_extractor = DatetimeExtractor(now=now, output_container='time',
                                           search_scope=search_scope,
                                           realistic_year_required=realistic_year_required,
                                           return_spans=return_spans)
    return datetime_extractor.parse_datetime(sentence=input_sentence)


def match_rules(now: datetime, sentence: str,
                search_scope: SearchScopes = SearchScopes.NOT_RESTRICTED,
                realistic_year_required: bool = True, return_spans: bool = False) -> Union[List, Dict[str, List]]:
    """
    Matches all rules against input text.
    :param now: Current timestamp to calculate relative dates.
    :param sentence: Input sentence.
    :param search_scope: Defines whether the timeframe should be restricted to past or future.
    :param realistic_year_required: Defines whether to restrict year candidates to be between 1900 and 2100.
    :param return_spans: Whether to include span information.
    :return: Parsed date and time classes.
    """
    matches = [*match_named_month(sentence, now, search_scope, return_spans),
               *match_iso_date(sentence, realistic_year_required, return_spans),
               *match_relative_day(sentence, now, return_spans),
               *match_weekday(sentence, now, search_scope, return_spans),
               *match_week(sentence, now, return_spans),
               *match_named_year(sentence, now, return_spans),
               *match_digi_clock(sentence, return_spans),
               *match_hwords(sentence, return_spans),
               *match_time_words(sentence, return_spans),
               *match_now(sentence, now, return_spans),
               *match_n_periods_compared_to_now(sentence, now, return_spans),
               *match_relative_month(sentence, now, return_spans),
               *match_in_past_n_periods(sentence, now, return_spans),
               *match_named_month_interval(sentence, return_spans),
               *match_named_month_start_mid_end(sentence, now, search_scope, return_spans),
               *match_day_of_month(sentence, now, return_spans)]

    if return_spans:
        # Collect spans from matches that have them
        spans = []
        for m in matches:
            if 'span' in m:
                spans.append(m['span'])

        # Extract date_parts as before
        date_parts = list(chain(*[m['date_parts'] for m in matches]))

        return {'date_parts': date_parts, 'spans': spans}
    else:
        # Original behavior - just return date_parts
        matches = list(chain(*[m['date_parts'] for m in matches]))
        return matches


def match_duration_rules(now: datetime, sentence: str,
                         search_scope: SearchScopes = SearchScopes.NOT_RESTRICTED,
                         realistic_year_required: bool = True) -> List:
    """
    Given that it as already been established that a duration is being parsed, matches all
    duration-specific rules against the input text.
    :param now: Current timestamp to calculate relative dates.
    :param sentence: Input sentence.
    :param search_scope: Defines whether the timeframe should be restricted to past or future.
    :param realistic_year_required: Defines whether to restrict year candidates to be between 1900 and 2100.
    :return: Parsed date and time classes.
    """
    matches = [
        *match_date_offset(sentence)
    ]

    matches = list(chain(*[m['date_parts'] for m in matches]))

    return matches


def extend_start_end(interval: Dict) -> Dict:
    """
    Heuristic to add missing date and time classes in case of interval.
    :param interval: Dictionary with start and end dateparts.
    :return: Extended dictionary with start and end dateparts.
    """
    if interval['start_date'] == 'OPEN' or interval['end_date'] == 'OPEN':
        return interval

    interval_ = copy(interval)
    for dp in interval['start_date']:
        if type(dp) not in [type(d) for d in interval['end_date']]:
            interval_['end_date'].append(dp)

    return interval_


def type_isin_list(date_type: type, lst: Union[List, str]) -> bool:
    if isinstance(lst, str):
        return False

    matches = [pot_dp for pot_dp in lst if isinstance(pot_dp, date_type)]

    return bool(matches)


class DatetimeExtractor:
    """
    This class handles combined date and time parsing.
    """

    def __init__(self, now: datetime = datetime.now(), output_container: str = 'datetime',
                 search_scope: SearchScopes = SearchScopes.NOT_RESTRICTED,
                 realistic_year_required: bool = True, return_spans: bool = False) -> None:
        """
        :param now: Current timestamp to calculate relative dates.
        :param output_container: datetime object to populate with datetime parts
        :param search_scope: Defines whether the timeframe should be restricted to past or future.
        :param realistic_year_required: Defines whether to restrict year candidates to be between 1900 and 2100.
        :param return_spans: Whether to include span information in the results.
        """
        self.now = now
        self.output_container = output_container
        self.search_scope = search_scope
        self.realistic_year_required = realistic_year_required
        self.return_spans = return_spans

    def _get_implicit_intervall(self, sentence_part: str):
        matches = match_rules(self.now, sentence_part, self.search_scope, self.realistic_year_required,
                              self.return_spans)
        if self.return_spans and isinstance(matches, dict):
            return [{'start_date': matches['date_parts'], 'end_date': matches['date_parts'],
                     'spans': matches['spans']}]
        else:
            return [{'start_date': matches, 'end_date': matches}]

    @return_on_value_error(None)
    def assemble_datetime(self, now: datetime,
                          dateparts: Union[List[Union[Year, Month, Week, Day, Daypart, Hour, Minute]], str],
                          bottom: bool = True) -> datelike:
        """
        Assambles parsed date and time classes into datetime instance.
        :param now: Current timestamp to calculate relative dates.
        :param dateparts: List of date and time classes.
        :param bottom: True if the bottom of the interval should be returned, False otherwise
        :param output_container: datetime object to populate with datetime parts
        :return: datetime instance
        """
        res_dt: List[int] = []

        if dateparts == 'OPEN':
            return None
        if not dateparts:
            return None

        has_date, has_time = False, False

        # this functionality is used to override the bottom or the top of the interval with the current date
        # rules indicate the necessity for this with returning either OverrideBottomWithNow or OverrideTopWithNow
        override_bottom, override_top = type_isin_list(OverrideBottomWithNow, dateparts), \
            type_isin_list(OverrideTopWithNow, dateparts)

        pre_first = True
        for date_type in [Year, Month, Week, Day, Daypart, Hour, Minute]:
            dp_match = [pot_dp for pot_dp in dateparts if isinstance(pot_dp, date_type)]

            _dp_match: Union[DateTimePartConatiner, None]
            if dp_match:
                _dp_match = dp_match[0]
            else:
                _dp_match = None

            if date_type == Year:
                if _dp_match and _dp_match.value is not None:
                    has_date = True
                    pre_first = False
                    res_dt.append(_dp_match.value)
                else:
                    # TODO: this should take into account the search_scope parameter...
                    res_dt.append(now.year)

            if date_type == Month:
                if _dp_match and _dp_match.value is not None:
                    has_date = True
                    pre_first = False
                    res_dt.append(_dp_match.value)
                elif pre_first:
                    res_dt.append(now.month)
                elif bottom:
                    res_dt.append(1)
                else:
                    res_dt.append(12)

            if date_type == Week and not type_isin_list(Day, dateparts):
                if _dp_match and _dp_match.value is not None:
                    has_date = True
                    pre_first = False
                    week2dt = monday_of_calenderweek(res_dt[0], _dp_match.value) + timedelta(days=(0 if bottom else 6))
                    res_dt = [week2dt.year, week2dt.month, week2dt.day]

            if date_type == Day and len(res_dt) == 2:
                if _dp_match and _dp_match.value is not None:
                    has_date = True
                    pre_first = False
                    res_dt.append(_dp_match.value)
                elif type_isin_list(StartDay, dateparts) and bottom:
                    res_dt.append(get_type_if_exists(dateparts, StartDay).value)
                elif type_isin_list(EndDay, dateparts) and not bottom:
                    res_dt.append(get_type_if_exists(dateparts, EndDay).value)
                elif pre_first:
                    res_dt.append(now.day)
                elif bottom:
                    res_dt.append(1)
                else:
                    mr = monthrange(res_dt[0], res_dt[1])
                    res_dt.append(mr[1])

            if date_type == Daypart:
                if _dp_match and _dp_match.value is not None:
                    has_time = True
                    pre_first = False
                    dp = _dp_match.value
                    if bottom:
                        res_dt.append(daypart_mapping[dp][0])
                    elif dp == 5:
                        y, m, d = res_dt
                        next_day = datetime(y, m, d) + timedelta(days=1)
                        res_dt = [next_day.year, next_day.month, next_day.day, daypart_mapping[dp][1]]
                    else:
                        res_dt.append(daypart_mapping[dp][1])

            if date_type == Hour and len(res_dt) == 3:
                if _dp_match and _dp_match.value is not None:
                    has_time = True
                    pre_first = False
                    res_dt.append(_dp_match.value)
                elif pre_first:
                    res_dt.append(now.hour)
                elif bottom:
                    res_dt.append(0)
                elif not bottom:
                    res_dt.append(23)

            if date_type == Minute:
                if _dp_match and _dp_match.value is not None:
                    has_time = True
                    pre_first = False
                    res_dt.append(_dp_match.value)
                elif pre_first:
                    res_dt.append(now.minute)
                elif bottom:
                    res_dt.append(0)
                elif not bottom:
                    res_dt.append(59)

        if bottom:
            res_dt.append(0)
        else:
            res_dt.append(59)

        y, m, d, h, mi, s = res_dt

        # Perform offsetting for duration parsing
        offset_objects: List = filter_offset_objects(dateparts)
        if offset_objects:
            y, m, d, h, mi, s = apply_offsets_and_return_components(y, m, d, h, mi, s, offset_objects)

        if self.output_container == 'datetime':
            if bottom and override_bottom:
                return now
            elif not bottom and override_top:
                return now
            elif has_date or has_time:
                return datetime(y, m, d, h, mi, s)
            else:
                return None
        elif self.output_container == 'date':
            if bottom and override_bottom:
                return now.date()
            elif not bottom and override_top:
                return now.date()
            elif has_date:
                return date(y, m, d)
            else:
                return None
        elif self.output_container == 'time':
            if bottom and override_bottom:
                return now.time()
            elif not bottom and override_top:
                return now.time()
            elif has_time:
                return time(h, mi, s)
            else:
                return None
        else:
            return None

    def parse_datetime(self, sentence: str) -> List[Dict[str, Any]]:
        """
        Fail-safe wrapper around _parse_datetime. All possible exceptions will be caught and an empty list is returned.
        """
        try:
            return self._parse_datetime(sentence)
        except Exception:
            return []

    def _parse_datetime(self, sentence: str) -> List[Dict[str, Any]]:
        """
        Extracts list of datetime intervals from input sentence.
        :param sentence: Input sentence string.
        :return: list of datetime interval dictionaries
        """
        sentence = sentence.lower()
        sentence_parts = match_multi_match(sentence)
        parsed_dates = []

        for sentence_part in sentence_parts:
            # Try to determine whether an explicit date interval has been provided
            # Something like holnap**tol** jovo kedd**ig**
            interval = match_interval(sentence_part)

            duration_parts = match_duration_match(sentence_part)

            # If explicit interval is detected, parse the start and end dates using that information...
            # For instance:
            #   holnap**tol** jovo kedd**ig**:
            #       start_date: parse_date(holnap)
            #       end_date: parse_date(jovo kedd)
            if interval and not duration_parts:
                start_result = (match_rules(self.now, interval['start_date'], self.search_scope,
                                            self.realistic_year_required, self.return_spans)
                                if interval['start_date'] != 'OPEN' else 'OPEN')
                end_result = (match_rules(self.now, interval['end_date'], self.search_scope,
                                          self.realistic_year_required, self.return_spans)
                              if interval['end_date'] != 'OPEN' else 'OPEN')

                if self.return_spans:
                    interval_spans = []
                    if isinstance(start_result, dict) and 'spans' in start_result:
                        interval_spans.extend(start_result['spans'])
                        interval['start_date'] = start_result['date_parts']
                    else:
                        interval['start_date'] = start_result

                    if isinstance(end_result, dict) and 'spans' in end_result:
                        interval_spans.extend(end_result['spans'])
                        interval['end_date'] = end_result['date_parts']
                    else:
                        interval['end_date'] = end_result

                    if interval_spans:
                        interval['spans'] = interval_spans
                else:
                    interval['start_date'] = start_result
                    interval['end_date'] = end_result
                parsed_dates.append(interval)

            # ... another way of explicitly expressing time intervals is with a start date and a duration
            # For instance:
            #   holnaptol 5 napig:
            #       start_date: parse_date(holnap)
            #       end_date: parse_date(holnap) + offset_with(5 days)
            elif duration_parts:
                from_part, duration_part = duration_parts

                start_result = match_rules(self.now, from_part, self.search_scope,
                                           self.realistic_year_required, self.return_spans)

                if self.return_spans and isinstance(start_result, dict):
                    interval['start_date'] = start_result['date_parts']
                    interval['end_date'] = (start_result['date_parts'] +
                                            match_duration_rules(self.now, duration_part,
                                                                 self.search_scope, self.realistic_year_required))
                    interval['spans'] = start_result['spans']
                else:
                    interval['start_date'] = start_result
                    interval['end_date'] = (start_result +
                                            match_duration_rules(self.now, duration_part,
                                                                 self.search_scope, self.realistic_year_required))
                parsed_dates.append(interval)

            # ... else try to determine a time interval implicitly.
            # For instance:
            #   holnap:
            #       start_date: parse_date(holnap, bottom=True) --> earliest datetime tomorrow
            #       end_date: parse_date(holnap, bottom=False)  --> latest datetime tomorrow
            else:
                parsed_dates += self._get_implicit_intervall(sentence_part)

        parsed_dates = [extend_start_end(intv) for intv in parsed_dates]

        if self.return_spans:
            # Include spans in final output
            result = []
            for parsed_date in parsed_dates:
                assembled = {
                    'start_date': self.assemble_datetime(self.now, parsed_date['start_date'], bottom=True),
                    'end_date': self.assemble_datetime(self.now, parsed_date['end_date'], bottom=False)
                }
                if 'spans' in parsed_date and parsed_date['spans']:
                    from hun_date_parser.utils import aggregate_spans
                    assembled['span'] = aggregate_spans(parsed_date['spans'])
                result.append(assembled)
            parsed_dates = result
        else:
            parsed_dates = [{'start_date': self.assemble_datetime(self.now, parsed_date['start_date'], bottom=True),
                             'end_date': self.assemble_datetime(self.now, parsed_date['end_date'], bottom=False)}
                            for parsed_date in parsed_dates]

        # remove results where
        # - both start and end dates are None
        # - or where the end date is smaller than the start
        parsed_dates = [
            intv for intv in parsed_dates if
            (intv['start_date'] or intv['end_date']) and
            is_smaller_date_or_none(intv['start_date'], intv['end_date'])
        ]

        return parsed_dates
