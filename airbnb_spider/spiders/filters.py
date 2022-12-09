from typing import Any


class Filters:

    def __init__(self, data):
        self.data = data

    def __setitem__(self, key, value):
        self._find(key=key)["filterValues"] = [str(value)]

    def _find(self, key: str) -> dict[str, Any]:
        items = list(filter(lambda d: d["filterName"] == key, self.data))
        if not items:
            item = {"filterName": key, "filterValues": None}
            self.data.append(item)
            return item

        return items[0]
