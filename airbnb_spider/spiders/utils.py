import datetime
import itertools
from collections import deque
from datetime import date, timedelta
from typing import Dict, Any


def dates(start_date, days):
    if start_date is None:
        start_date = date.today()
    start_date = start_date if isinstance(start_date, date) else date.fromisoformat(start_date)
    base = start_date
    dates = [base + timedelta(days=x) for x in range(days)]
    return list(map(str, dates))


def format_dict(d):
    return ' '.join([f'{k}:{v}' for k, v in d.items()])


def to_date(date_str: str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()


def from_date(dt: date):
    return dt.strftime("%Y-%m-%d")


def dates_generator(start_date, end_date, step=7):
    step = datetime.timedelta(days=step)
    while start_date <= end_date:
        yield start_date, start_date + step
        start_date += step


def normalize(d: Dict[str, Any]) -> Dict[str, Any]:
    result = {}

    def _normalize(d, keys=deque()):
        for k, v in d.items():
            if k.startswith("__"):
                continue
            if isinstance(v, list):
                continue
            if isinstance(v, dict):
                _normalize(d=v, keys=keys + deque([k]))
                continue
            keys_str = "_".join(keys + deque([k]))
            result[keys_str] = v
        return result

    return _normalize(d=d)


def iterate_prices(start, end, step):
    it1, it2 = itertools.tee(range(start, end + step, step))
    next(it2)
    for i, j in zip(it1, it2):
        yield i, j
    yield j, None
