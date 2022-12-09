import dataclasses
import logging
from datetime import date
import jsonpath_ng
import requests

from airbnb_spider.spiders import constants

log = logging.getLogger(__name__)


class Place:

    @staticmethod
    def from_query(query: str) -> 'Place':
        resp = requests.get(url=constants.AUTO_COMPLETE_URL.format(query=query))
        resp.raise_for_status()
        data = resp.json()["autocomplete_terms"][0]["explore_search_params"]
        place = Place(id=data["place_id"], query=data["query"])
        log.info(f'Autompleting:{query=}. Result: {place=}')
        return place

    def __init__(self, id: str, query: str) -> None:
        self.id = id
        self.query = query
        self.on_new_item = lambda item: None

    def __str__(self):
        return f"Place(id={self.id} query={self.query})"

    __repr__ = __str__

    def _get_prices_range(self, start_date: date, end_date: date):
        data = self._request(start_date=start_date, end_date=end_date)
        expr = jsonpath_ng.parse("$.data.presentation.explore.sections.sections[*].section.discreteFilterItems[*].[minValue,maxValue]")
        prices = [item.value for item in expr.find(data)]
        assert len(prices) == 2
        return prices

