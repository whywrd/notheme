from pages.page import Page
from pages.components.blog_info import SubdomainDescription, FullSubdomainDescription, UserDescription,\
    UserBlogDescription
from constants import responses as RespC
import flask


class InfoPage(Page):

    INFO_TEMPLATE = 'info/info.html'

    def build_content(self, json):
        raise NotImplementedError

    def build_meta_info(self, json):
        raise NotImplementedError

    def render_descriptions(self):
        for description in self.content:
            yield flask.render_template(self.INFO_TEMPLATE, page=self, description=description)


class SubdomainInfoPage(InfoPage):

    """
    content is a dictionary of information. meta info is the blog subdomain and name
    """

    def build_content(self, json):
        return [SubdomainDescription(json[RespC.Response.BLOG_INFO])]

    def build_meta_info(self, json):
        blog_info = json[RespC.Response.BLOG_INFO]
        name = blog_info[RespC.BlogInfo.NAME]
        title = blog_info[RespC.BlogInfo.TITLE]
        if not title:
            title = name
        return {RespC.BlogInfo.TITLE: title,
                RespC.BlogInfo.NAME: name,
                RespC.BlogInfo.SHARE_LIKES: blog_info[RespC.BlogInfo.SHARE_LIKES]}


class UserInfoPage(InfoPage):

    """
    content is dictionary of user information. meta info is the user
    """

    def build_content(self, json):
        info = UserDescription(json[RespC.UserInfo.USER])
        blogs = [UserBlogDescription(blog) for blog in json[RespC.UserInfo.USER][RespC.UserInfo.BLOGS]]
        return [info, *blogs]

    def build_meta_info(self, json):
        user_info = json[RespC.UserInfo.USER]
        return {RespC.BlogInfo.TITLE: user_info[RespC.UserInfo.NAME],
                RespC.UserInfo.NAME: user_info[RespC.UserInfo.NAME]}


class FollowingPage(InfoPage):

    """
    content is a list of blog info dictionaries
    """

    def build_content(self, json):
        return [FullSubdomainDescription(blog) for blog in json[RespC.Response.BLOGS_INFO]]

    def build_meta_info(self, json):
        return json[RespC.Response.TOTAL_BLOGS]


class FollowersPage(InfoPage):

    """
    content is a list of blog info dictionaries
    """

    def build_content(self, json):
        return [FullSubdomainDescription(blog) for blog in json[RespC.Response.USERS]]

    def build_meta_info(self, json):
        return json[RespC.Response.TOTAL_USERS]
