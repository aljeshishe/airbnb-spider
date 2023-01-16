import datetime
import itertools
from collections import deque
from datetime import date, timedelta
from itertools import tee
from typing import Dict, Any, Optional

import numpy as np

from airbnb_spider.lib.bbox import BBox


def dates(start_date, days):
    if start_date is None:
        start_date = date.today()
    start_date = start_date if isinstance(start_date, date) else date.fromisoformat(start_date)
    base = start_date
    dates = [base + timedelta(days=x) for x in range(days)]
    return list(map(str, dates))


def format_dict(d):
    return ' '.join([f'{k}:{v}' for k, v in d.items()])


def to_date(date_str: Optional[str]):
    if date_str is None:
        return None
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()


def from_date(dt: date):
    return dt.strftime("%Y-%m-%d")


def dates_generator(start_date, end_date, step=7):
    step = datetime.timedelta(days=step)
    while start_date < end_date:
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


def gen_ranges(start, end, steps):
    g1, g2 = tee(np.linspace(start, end, steps + 1, endpoint=True))
    next(g2)
    for start, end in zip(g1, g2):
        yield start, end

def as_bboxes(bboxes_str:str) -> list[BBox]:
    """Converts bboxes_str"""
    result = []
    for line in bboxes_str.splitlines():
        line = line.strip().replace("http://bboxfinder.com/#", "")
        if not line:
            continue
        bbox = BBox(*map(float, line.split(",")))
        result.append(bbox)
    return result

def check_port(port):
    """Check if port is free"""
    import socket
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    try:
        s.bind(("", port))
        s.close()
        return True
    except socket.error:
        return False

def get_free_port(port):
    for p in range(port, 65535):
        if check_port(p):
            return p
