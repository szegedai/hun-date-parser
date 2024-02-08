from typing import List, Union, Any
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from . import MinuteOffset, HourOffset, DayOffset, MonthOffset, YearOffset


# Function to convert a list of objects into a dict suitable for the add_time function
def convert_to_dict(offset_list: List[Union[MinuteOffset, HourOffset, DayOffset, MonthOffset, YearOffset]]) -> dict:
    param_dict = {'years': 0, 'months': 0, 'days': 0, 'hours': 0, 'minutes': 0}
    for item in offset_list:
        if isinstance(item, MinuteOffset):
            param_dict['minutes'] = item.value if item.value is not None else 0
        elif isinstance(item, HourOffset):
            param_dict['hours'] = item.value if item.value is not None else 0
        elif isinstance(item, DayOffset):
            param_dict['days'] = item.value if item.value is not None else 0
        elif isinstance(item, MonthOffset):
            param_dict['months'] += item.value if item.value is not None else 0
        elif isinstance(item, YearOffset):
            param_dict['years'] += item.value if item.value is not None else 0

    return param_dict


def add_time(original_datetime, years=0, months=0, weeks=0, days=0, hours=0, minutes=0):
    """
    Add specified time to a datetime object.

    Parameters:
    - original_datetime: datetime.datetime object to add time to.
    - years, months, weeks, days, hours, minutes: Integers representing the amount of time to add.

    Returns:
    - A datetime.datetime object with the specified time added.
    """
    # Add years and months using relativedelta for accurate adjustments
    new_datetime = original_datetime + relativedelta(years=years, months=months)

    # Add weeks, days, hours, and minutes using timedelta
    new_datetime += timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes)

    return new_datetime


def apply_offsets_and_return_components(
        y: int, m: int, d: int, h: int, mi: int, s: int,
        offset_list: List[Union[MinuteOffset, HourOffset, DayOffset, MonthOffset, YearOffset]]
) -> tuple:
    param_dict: dict = convert_to_dict(offset_list)
    original_datetime = datetime(y, m, d, h, mi, s)
    new_datetime: datetime = add_time(original_datetime, **param_dict)
    return (new_datetime.year, new_datetime.month, new_datetime.day,
            new_datetime.hour, new_datetime.minute, new_datetime.second)


def filter_offset_objects(input_list: Union[List[Any], str]) -> List[Any]:
    """
    Filters the input list to keep only the offset objects (DayOffset, MonthOffset, YearOffset).

    Parameters:
    - input_list: List containing a mix of different types.

    Returns:
    - A list containing only DayOffset, MonthOffset, and YearOffset objects.
    """
    if isinstance(input_list, str):
        return []

    # Filter the list to include only instances of DayOffset, MonthOffset, or YearOffset
    filtered_list: List[Union[DayOffset, MonthOffset, YearOffset]] = [
        item for item in input_list if isinstance(item, (DayOffset, MonthOffset, YearOffset))
    ]

    return filtered_list
