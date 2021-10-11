from datetime import datetime

from hun_date_parser import text2datetime


def extract_within_interval(interval_start: datetime, interval_end: datetime, query_text: str):
    res = text2datetime(query_text, now=interval_start)

    res_filt = []
    for r in res:
        if interval_start <= r['start_date'] and r['end_date'] <= interval_end:
            res_filt.append(r)

    return res_filt
