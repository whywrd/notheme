from tumblr_api_handler.params import params
from datetime import datetime
from constants import posts as Pc

DEFAULT_LIMIT = 10


class InfoParams(params.Params):
    pass


class DashboardParams(params.Params):
    def __init__(self):
        super().__init__()
        self.limit = params.QueryStringParam('limit', False, int, DEFAULT_LIMIT)
        self.offset = params.QueryStringParam('offset', False, int)
        self.post_type = params.QueryStringParam('type', False, Pc.Types)
        self.since_post_id = params.QueryStringParam('since_id', False, int)
        self.reblog_info = params.QueryStringParam('reblog_info', False, bool, getter_lambda=lambda x: 'true' if x else 'false')
        self.notes_info = params.QueryStringParam('notes_info', False, bool, getter_lambda=lambda x: 'true' if x else 'false')


class LikesParams(params.Params):
    def __init__(self):
        super().__init__()
        self.limit = params.QueryStringParam('limit', False, int, DEFAULT_LIMIT)
        self.offset = params.QueryStringParam('offset', False, int)
        self.before = params.QueryStringParam('before', False, datetime, getter_lambda=lambda x: x.timestamp())
        self.after = params.QueryStringParam('after', False, datetime, getter_lambda=lambda x: x.timestamp())


class FollowingParams(params.Params):
    def __init__(self):
        super().__init__()
        self.limit = params.QueryStringParam('limit', False, int, DEFAULT_LIMIT)
        self.offset = params.QueryStringParam('offset', False, int)


class FollowParams(params.Params):
    def __init__(self):
        super().__init__()
        self.url = params.POSTDataParam('url', True, str)


class UnfollowParams(params.Params):
    def __init__(self):
        super().__init__()
        self.url = params.POSTDataParam('url', True, str)


class LikeParams(params.Params):
    def __init__(self):
        super().__init__()
        self.post_id = params.POSTDataParam('id', True, str)
        self.reblog_key = params.POSTDataParam('reblog_key', True, str)


class UnlikeParams(params.Params):
    def __init__(self):
        super().__init__()
        self.post_id = params.POSTDataParam('id', True, str)
        self.reblog_key = params.POSTDataParam('reblog_key', True, str)
