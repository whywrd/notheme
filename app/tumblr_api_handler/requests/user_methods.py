from tumblr_api_handler.requests import requests
from tumblr_api_handler.params import user_method_params as ps


class InfoQuery(requests.GETRequest):

    def __init__(self, params: ps.InfoParams):
        super().__init__('api.tumblr.com/v2/user/info', params)


class DashboardQuery(requests.GETRequest):

    def __init__(self, params: ps.DashboardParams):
        super().__init__('api.tumblr.com/v2/user/dashboard', params)


class LikesQuery(requests.GETRequest):

    def __init__(self, params: ps.LikesParams):
        super().__init__('api.tumblr.com/v2/user/likes', params)


class FollowingQuery(requests.GETRequest):

    def __init__(self, params: ps.FollowingParams):
        super().__init__('api.tumblr.com/v2/user/following', params)


class FollowQuery(requests.POSTRequest):

    def __init__(self, params: ps.FollowParams):
        super().__init__('api.tumblr.com/v2/user/follow', params)


class UnfollowQuery(requests.POSTRequest):

    def __init__(self, params: ps.UnfollowParams):
        super().__init__('api.tumblr.com/v2/user/unfollow', params)


class LikeQuery(requests.POSTRequest):

    def __init__(self, params: ps.LikeParams):
        super().__init__('api.tumblr.com/v2/user/like', params)


class UnlikeQuery(requests.POSTRequest):

    def __init__(self, params: ps.UnlikeParams):
        super().__init__('api.tumblr.com/v2/user/unlike', params)

