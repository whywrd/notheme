from tumblr_api_handler.params import params
from datetime import datetime
from constants import posts as Pc

DEFAULT_LIMIT = 20


class TaggedParams(params.Params):
    def __init__(self):
        self.api_key = params.QueryStringParam('api_key', True, str)
        self.tag = params.QueryStringParam('tag', True, str)
        self.before = params.QueryStringParam('before', False, str)
        self.limit = params.QueryStringParam('limit', False, int, DEFAULT_LIMIT)
        self.post_filter = params.QueryStringParam('filter', False, Pc.PostFilter)
