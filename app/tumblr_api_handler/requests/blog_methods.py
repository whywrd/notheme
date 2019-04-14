from tumblr_api_handler.requests import requests
import tumblr_api_handler.params.blog_method_params as ps


class InfoQuery(requests.GETRequest):

    def __init__(self, params: ps.InfoParams):
        super().__init__('api.tumblr.com/v2/blog/{blog-identifier}/info',
                         params)


class AvatarQuery(requests.GETRequest):

    def __init__(self, params: ps.AvatarParams):
        super().__init__('api.tumblr.com/v2/blog/{blog-identifier}/avatar{size}',
                         params)


class LikesQuery(requests.GETRequest):

    def __init__(self, params: ps.LikesParams):
        super().__init__('api.tumblr.com/v2/blog/{blog-identifier}/likes',
                         params)


class FollowingQuery(requests.GETRequest):
    
    def __init__(self, params: ps.FollowingParams):
        super().__init__('api.tumblr.com/v2/blog/{blog-identifier}/following',
                         params)
        

class FollowersQuery(requests.GETRequest):
    
    def __init__(self, params: ps.FollowersParams):
        super().__init__('api.tumblr.com/v2/blog/{blog-identifier}/followers',
                         params)


class PostsQuery(requests.GETRequest):

    def __init__(self, params: ps.PostsParams):
        super().__init__('api.tumblr.com/v2/blog/{blog-identifier}/posts{type}',
                         params)


class QueueQuery(requests.GETRequest):

    def __init__(self, params: ps.QueueParams):
        super().__init__('api.tumblr.com/v2/blog/{blog-identifier}/posts/queue',
                         params)


class DraftQuery(requests.GETRequest):

    def __init__(self, params: ps.DraftParams):
        super().__init__('api.tumblr.com/v2/blog/{blog-identifier}/posts/draft',
                         params)


class SubmissionQuery(requests.GETRequest):

    def __init__(self, params: ps.SubmissionParams):
        super().__init__('api.tumblr.com/v2/blog/{blog-identifier}/posts/submission',
                         params)


class CreatePostQuery(requests.POSTRequest):

    """
    params Should be of a Create<POSTTYPE>PostParms type
    """

    def __init__(self, params: ps.PostPOSTParams):
        super().__init__('api.tumblr.com/v2/blog/{blog-identifier}/post',
                         params)


class EditPostQuery(requests.POSTRequest):

    """
    params should be of an Edit<POSTTYPE>PostParams type
    """

    def __init__(self, params: ps.PostPOSTParams):
        super().__init__('api.tumblr.com/v2/blog/{blog-identifier}/post/edit',
                         params)


class ReblogPostQuery(requests.POSTRequest):

    def __init__(self, params: ps.ReblogPostParams):
        super().__init__('api.tumblr.com/v2/blog/{blog-identifier}/post/reblog',
                         params)


class DeletePostQuery(requests.POSTRequest):

    def __init__(self, params: ps.DeletePostParams):
        super().__init__('api.tumblr.com/v2/blog/{blog-identifier}/post/delete',
                         params)
