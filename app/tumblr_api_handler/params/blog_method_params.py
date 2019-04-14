from tumblr_api_handler.params import params
from datetime import datetime

DEFAULT_LIMIT = 10


class BlogMethodParams(params.Params):
    def __init__(self):
        self.blog_identifier = params.BaseURLParam('blog-identifier', True, str)


class InfoParams(BlogMethodParams):
    def __init__(self):
        super().__init__()
        self.api_key = params.QueryStringParam('api_key', True, str)


class AvatarParams(BlogMethodParams):
    def __init__(self):
        super().__init__()
        self.size = params.BaseURLParam('size', False, int, 64, getter_lambda=lambda x: '/{}'.format(x) if x else '')


class LikesParams(BlogMethodParams):
    def __init__(self):
        super().__init__()
        self.api_key = params.QueryStringParam('api_key', True, str)
        self.limit = params.QueryStringParam('limit', False, int, DEFAULT_LIMIT)
        self.offset = params.QueryStringParam('offset', False, int)
        self.before = params.QueryStringParam('before', False, datetime, getter_lambda=lambda x: x.timestamp())
        self.after = params.QueryStringParam('after', False, datetime, getter_lambda=lambda x: x.timestamp())


class FollowingParams(BlogMethodParams):
    def __init__(self):
        super().__init__()
        self.limit = params.QueryStringParam('limit', False, int, DEFAULT_LIMIT)
        self.offset = params.QueryStringParam('offset', False, int)
        self.query = params.QueryStringParam('query', False, str)


class FollowersParams(BlogMethodParams):
    def __init__(self):
        super().__init__()
        self.limit = params.QueryStringParam('limit', False, int)
        self.offset = params.QueryStringParam('offset', False, int)


class PostsParams(BlogMethodParams):
    def __init__(self):
        super().__init__()
        self.api_key = params.QueryStringParam('api_key', True, str)
        self.post_type = params.BaseURLParam('type', False, str, '', getter_lambda=lambda x: '/{}'.format(x))
        self.post_id = params.QueryStringParam('id', False, int)
        self.tag = params.QueryStringParam('tag', False, str)
        self.limit = params.QueryStringParam('limit', False, int, DEFAULT_LIMIT)
        self.offset = params.QueryStringParam('offset', False, int)
        self.reblog_info = params.QueryStringParam('reblog_info', False, bool, getter_lambda=lambda x: 'true' if x else 'false')
        self.notes_info = params.QueryStringParam('notes_info', False, bool, getter_lambda=lambda x: 'true' if x else 'false')
        self.post_format = params.QueryStringParam('filter', False, str)


class NotesParams(BlogMethodParams):
    def __init__(self):
        super().__init__()
        self.api_key = params.QueryStringParam('api_key', True, str)


class QueueParams(BlogMethodParams):
    def __init__(self):
        super().__init__()
        self.offset = params.QueryStringParam('offset', False, int)
        self.limit = params.QueryStringParam('limit', False, int, DEFAULT_LIMIT)
        self.post_format = params.QueryStringParam('filter', False, str)


class DraftParams(BlogMethodParams):
    def __init__(self):
        super().__init__()
        self.before_id = params.QueryStringParam('before_id', False, int)
        self.post_format = params.QueryStringParam('filter', False, str)


class SubmissionParams(BlogMethodParams):
    def __init__(self):
        super().__init__()
        self.offset = params.QueryStringParam('offset', False, int)
        self.post_format = params.QueryStringParam('filter', False, str)


class PostPOSTParams(BlogMethodParams):
    def __init__(self):
        super().__init__()
        self.post_type = params.POSTDataParam('type', False, str)
        self.state = params.POSTDataParam('state', False, str)
        self.tags = params.POSTDataParam('tags', False, list, getter_lambda=lambda x: ','.join(x))
        self.tweet = params.POSTDataParam('tweet', False, str)
        self.date = params.POSTDataParam('date', False, datetime, getter_lambda=lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        self.post_format = params.POSTDataParam('format', False, str, str)
        self.slug = params.POSTDataParam('slug', False, str)
        self.native_inline_images = params.POSTDataParam('native_inline_images', False, bool, getter_lambda=lambda x: 'true' if x else 'false')


class CreateTextPostParams(PostPOSTParams):
    def __init__(self):
        super().__init__()
        self.title = params.POSTDataParam('title', False, str)
        self.body = params.POSTDataParam('body', True, str)


class CreatePhotoPostParams(PostPOSTParams):
    """
    one of either source, data or data64 is required.
    """
    def __init__(self):
        super().__init__()
        self.caption = params.POSTDataParam('caption', False, str)
        self.link = params.POSTDataParam('link', False, str)
        self.source = params.POSTDataParam('source', False, str)
        self.data = params.POSTDataParam('data', False, list, getter_lambda=lambda x: ','.join(x))
        self.data64 = params.POSTDataParam('data', False, str)


class CreateQuotePostParams(PostPOSTParams):
    def __init__(self):
        super().__init__()
        self.quote = params.POSTDataParam('quote', True, str)
        self.source = params.POSTDataParam('source', False, str)


class CreateLinkPostParams(PostPOSTParams):
    def __init__(self):
        super().__init__()
        self.title = params.POSTDataParam('title', False, str)
        self.url = params.POSTDataParam('url', True, str)
        self.description = params.POSTDataParam('description', False, str)
        self.thumbnail = params.POSTDataParam('thumbnail', False, str)
        self.excerpt = params.POSTDataParam('excerpt', False, str)
        self.author = params.POSTDataParam('author', False, str)


class CreateChatPostParams(PostPOSTParams):
    def __init__(self):
        super().__init__()
        self.title = params.POSTDataParam('title', False, str)
        self.conversation = params.POSTDataParam('conversation', True, str)


class CreateAudioPostParams(PostPOSTParams):
    """
    one of either embed or data are required
    """
    def __init__(self):
        super().__init__()
        self.caption = params.POSTDataParam('caption', False, str)
        self.embed = params.POSTDataParam('embed', False, str)
        self.data = params.POSTDataParam('data', False, str)


class EditPostParams(PostPOSTParams):
    def __init__(self):
        super().__init__()
        self.post_id = params.POSTDataParam('id', True, int)


class ReblogPostParams(PostPOSTParams):
    def __init__(self):
        super().__init__()
        self.post_id = params.POSTDataParam('id', True, str)
        self.reblog_key = params.POSTDataParam('reblog_key', True, str)
        self.comment = params.POSTDataParam('comment', False, str)


class DeletePostParams(BlogMethodParams):
    def __init__(self):
        super().__init__()
        self.post_id = params.POSTDataParam('id', True, str)
