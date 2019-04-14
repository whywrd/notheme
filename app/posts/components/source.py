from utils.url_utils import TumblrDomainUtils
from flask import url_for
from constants import routes as Rc, responses as RespC


class Source(dict):
    """
    Dictionary containing information about the source of a post
    keys:
         via -> the name of the blog the post is reblogged from
         via_url -> the url for the blog the post is reblogged from
         source -> the name of the blog the post originated from
         source_url -> the url for the blog the post originated from
         blog_name -> the short name of the blog the post is from
         blog_name_href -> the url generated from the blog short name
    """

    def __init__(self, json):
        super(Source, self).__init__(self.construct(json))

    @staticmethod
    def construct(json):
        via = json.get(RespC.Post.REBLOGGED_FROM_NAME)
        via_url = json.get(RespC.Post.REBLOGGED_FROM_URL)
        if via_url:
            via_url = TumblrDomainUtils.to_noneblr(via_url)

        source = json.get(RespC.Post.SOURCE_TITLE)
        source_url = json.get(RespC.Post.SOURCE_URL)
        if source_url:
            source_url = TumblrDomainUtils.to_noneblr(source_url)

        blog = json.get(RespC.Post.BLOG_NAME)
        blog_url = url_for(Rc.Subdomains.POSTS_PAGE, subdomain=blog)

        return {'via': via,
                'via_url': via_url,
                'source': source,
                'source_url': source_url,
                'blog': blog,
                'blog_url': blog_url}
