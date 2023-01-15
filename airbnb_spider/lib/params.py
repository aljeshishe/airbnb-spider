from typing import Optional

import attr

from airbnb_spider.lib import utils
from airbnb_spider.lib.bbox import BBox


@attr.define
class Params:
    name: str
    start_date: str = attr.field(converter=utils.to_date)
    end_date: str = attr.field(converter=utils.to_date)
    bbox: Optional[BBox] = None
    bboxes_str: Optional[str] = None
