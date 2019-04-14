from constants import routes as Rc
from flask import url_for
from math import ceil


class Navigation:

    def __init__(self, page_number, limit, total, route: Rc, **route_kwargs):
        self._limit = limit
        self.page_number = page_number
        self._total = total
        self._route = route
        self._route_kwargs = route_kwargs

    @property
    def total_pages(self):
        if not self._total:
            total_pages = float('inf')
        else:
            total_pages = ceil(self._total / self._limit)
        return total_pages

    @property
    def include_next(self):
        return self.page_number < self.total_pages

    @property
    def include_prev(self):
        return self.page_number != 1

    def url_for_next_page(self):
        return url_for(self._route, page_number=self.page_number + 1, **self._route_kwargs)

    def url_for_prev_page(self):
        return url_for(self._route, page_number=self.page_number - 1, **self._route_kwargs)
