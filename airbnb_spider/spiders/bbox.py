from datetime import date

import jsonpath_ng
from attr import define


@define
class BBox:
    sw_lat: float
    sw_lng: float
    ne_lat: float
    ne_lng: float

    def __str__(self):
        return f"{self.__class__.__name__}({self.sw_lat:.6f},{self.sw_lng:.6f},{self.ne_lat:.6f},{self.ne_lng:.6f})"

    __repr__ = __str__

    def _get_prices_range(self, start_date: date, end_date: date):
        data = self._request(start_date=start_date, end_date=end_date)
        expr = jsonpath_ng.parse("$.data.presentation.explore.sections.sections[*].section.discreteFilterItems[*].[minValue,maxValue]")
        prices = [item.value for item in expr.find(data)]
        assert len(prices) == 2
        return prices

