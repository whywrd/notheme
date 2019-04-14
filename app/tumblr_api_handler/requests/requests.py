from tumblr_api_handler.params import params as ps
from urllib.parse import urlencode


class Request:

    def __init__(self, base_url: str, params: ps.Params):
        self._base_url = base_url
        self.params = params

    @property
    def base_url(self):
        return 'http://' + self._base_url.format(**self.params.of_type(ps.BaseURLParam))

    @property
    def url(self):
        raise NotImplementedError


class GETRequest(Request):

    @property
    def url(self):
        query_string = urlencode(self.params.of_type(ps.QueryStringParam))
        return self.base_url + '?' + query_string


class POSTRequest(Request):

    @property
    def url(self):
        return self.base_url

    @property
    def data(self):
        return self.params.of_type(ps.POSTDataParam)
