from pages.page import Page
from constants import responses as RespC, session as SeshC
from posts import factory
import flask


class LikesPage(Page):

    """
    content is a list of posts. meta info is the blog subdomain and name
    """

    def __init__(self, info_json, json):
        json.update(info_json)
        super().__init__(json)

    def build_content(self, json):
        raw_posts = json[RespC.Response.LIKED_POSTS]
        posts = (factory.Factory.create(x) for x in raw_posts)
        return posts

    def build_meta_info(self, json):
        blog_info = json[RespC.Response.BLOG_INFO]
        return {RespC.BlogInfo.NAME: blog_info[RespC.BlogInfo.NAME],
                RespC.BlogInfo.TITLE: blog_info[RespC.BlogInfo.TITLE]}

    @property
    def is_user_blog(self):
        return self.meta_info[RespC.BlogInfo.NAME] in flask.session.get(SeshC.USER_BLOGS, [])

    def render_posts(self):
        for post in self.content:
            yield flask.render_template('posts/post.html', page=self, post=post)
