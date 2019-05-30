from pages.page import Page
from constants import responses as RespC, session as SeshC, forms as FormC
from posts import factory
import logging
import flask

DASHBOARD_TITLE = 'dashboard'
TAGGED_TITLE = 'tagged'


class PostPage(Page):

    """
    content is a list of posts. meta info is the blog subdomain and name
    """

    POST_TEMPLATE = 'posts/post.html'

    def build_content(self, json):
        raw_posts = json[RespC.Response.POSTS]
        posts = (factory.Factory.create(x) for x in raw_posts)
        return posts

    def build_meta_info(self, json):
        raise NotImplementedError

    def render_posts(self, **kwargs):
        for post in self.content:
            yield flask.render_template(self.POST_TEMPLATE, page=self, post=post, is_mobile=flask.request.MOBILE,
                                        **kwargs)


class SubdomainPostPage(PostPage):

    """
    content is a list of posts. meta info is the blog subdomain and name
    """

    def build_meta_info(self, json):
        logging.debug(json)
        blog_info = json[RespC.Response.BLOG_INFO]
        name = blog_info[RespC.BlogInfo.NAME]
        title = blog_info[RespC.BlogInfo.TITLE]
        followed = blog_info.get(RespC.BlogInfo.FOLLOWED, False)
        if not title:
            title = name
        return {RespC.BlogInfo.NAME: name,
                RespC.BlogInfo.TITLE: title,
                RespC.BlogInfo.FOLLOWED: followed}

    @property
    def is_user_blog(self):
        return self.meta_info[RespC.BlogInfo.NAME] in flask.session.get(SeshC.USER_BLOGS, [])

    def render_posts(self, **kwargs):
        return super().render_posts(include_delete=self.is_user_blog)


class DashboardPostPage(PostPage):

    """
    content is a list of posts. there is no meta info associated with the dashboard response.
    """

    def build_meta_info(self, json):
        return {RespC.BlogInfo.TITLE: DASHBOARD_TITLE}

    def render_posts(self, **kwargs):
        return super().render_posts(is_dashboard=True)


class TaggedPostPage(PostPage):

    """
    content is a list of posts. there is no meta info associated with the dashboard response.
    """

    def build_meta_info(self, json):
        return {RespC.BlogInfo.TITLE: TAGGED_TITLE}


class ReblogPostPage(PostPage):

    """
    content is the post. meta info contains blog name and title, reblog key, and list of user blogs that can be
    reblogged to in the order to be displayed on the reblog page
    """

    POST_TEMPLATE = 'posts/reblog.html'

    def __init__(self, user_info_json, json):
        json.update(user_info_json)
        super().__init__(json)

    def build_meta_info(self, json):
        return {RespC.BlogInfo.NAME: json[RespC.Response.BLOG_INFO][RespC.BlogInfo.NAME],
                RespC.BlogInfo.TITLE: json[RespC.Response.BLOG_INFO][RespC.BlogInfo.TITLE],
                FormC.Reblog.BLOG_IDENTIFIERS: self.get_blog_list(json)}

    @staticmethod
    def get_blog_list(json):
        blogs = json[RespC.UserInfo.USER][RespC.UserInfo.BLOGS]
        primary_blog = [blog[RespC.BlogInfo.NAME] for blog in blogs if blog[RespC.BlogInfo.PRIMARY]]
        other_blogs = [blog[RespC.BlogInfo.NAME] for blog in blogs if not blog[RespC.BlogInfo.PRIMARY]]
        blogs = primary_blog + other_blogs
        return blogs
