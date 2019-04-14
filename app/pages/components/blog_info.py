from utils.url_utils import TumblrDomainUtils
from utils.html_utils import BuildHtmlUtils
from constants import responses as RespC, routes as Rc
from collections import OrderedDict
import flask

BLOG_COUNT = 'blogs'
BLOG_NAME = 'blog_name'
LINKS = 'links'
USERNAME = 'username'


class Description:

    _keys = []

    def __init__(self, json):
        self._raw = json

    @property
    def links(self) -> list:
        raise NotImplementedError

    @property
    def description(self):
        return self.format_description(self.construct_description(self._raw, self.links))

    @classmethod
    def format_description(cls, descr):
        raise NotImplementedError

    @classmethod
    def construct_description(cls, raw, links) -> OrderedDict:
        descr = OrderedDict()
        descr[LINKS] = '[{}]'.format(', '.join([link.prettify() for link in links]))
        for key in cls._keys:
            if key in raw:
                descr[key] = raw[key]
        return descr


class FullSubdomainDescription(Description):

    _keys = [RespC.BlogInfo.NAME,
             RespC.BlogInfo.TITLE,
             RespC.BlogInfo.URL,
             RespC.BlogInfo.DESCRIPTION,
             RespC.BlogInfo.IS_ADULT,
             RespC.BlogInfo.IS_NSFW,
             RespC.BlogInfo.POSTS,
             RespC.BlogInfo.LIKES,
             RespC.BlogInfo.SHARE_FOLLOWING,
             RespC.BlogInfo.SHARE_LIKES]

    @property
    def links(self):
        links = []
        posts = flask.url_for(Rc.Subdomains.POSTS_PAGE, subdomain=self._raw[RespC.BlogInfo.NAME])
        links.append(BuildHtmlUtils.to_href(posts, 'posts'))
        if self._raw.get(RespC.BlogInfo.SHARE_LIKES, False):
            url = flask.url_for(Rc.Subdomains.LIKES, subdomain=self._raw[RespC.BlogInfo.NAME])
            links.append(BuildHtmlUtils.to_href(url, 'likes'))
        info = flask.url_for(Rc.Subdomains.INFO, subdomain=self._raw[RespC.BlogInfo.NAME])
        links.append(BuildHtmlUtils.to_href(info, 'info'))
        if self._raw.get(RespC.BlogInfo.SHARE_FOLLOWING, False):
            url = flask.url_for(Rc.Subdomains.FOLLOWING, subdomain=self._raw[RespC.BlogInfo.NAME])
            links.append(BuildHtmlUtils.to_href(url, Rc.Subdomains.FOLLOWING))
        return links

    @classmethod
    def format_description(cls, descr):
        if RespC.BlogInfo.TITLE in descr:
            descr.move_to_end(RespC.BlogInfo.TITLE, last=False)
        if RespC.BlogInfo.NAME in descr:
            descr.move_to_end(RespC.BlogInfo.NAME, last=False)
        descr[RespC.BlogInfo.URL] = BuildHtmlUtils.to_href(descr[RespC.BlogInfo.URL])
        return descr


class SubdomainDescription(Description):

    _keys = [RespC.BlogInfo.NAME,
             RespC.BlogInfo.URL,
             RespC.BlogInfo.DESCRIPTION,
             RespC.BlogInfo.IS_ADULT,
             RespC.BlogInfo.IS_NSFW,
             RespC.BlogInfo.POSTS,
             RespC.BlogInfo.LIKES,
             RespC.BlogInfo.SHARE_FOLLOWING,
             RespC.BlogInfo.SHARE_LIKES]

    @property
    def links(self):
        return []

    @classmethod
    def format_description(cls, descr):
        descr.pop(LINKS)
        descr[RespC.BlogInfo.URL] = BuildHtmlUtils.to_href(descr[RespC.BlogInfo.URL])
        return descr


class UserDescription(Description):

    _keys = [RespC.UserInfo.NAME,
             RespC.UserInfo.BLOGS,
             RespC.UserInfo.FOLLOWING]

    @property
    def links(self):
        return []

    @classmethod
    def format_description(cls, descr):
        descr.pop(LINKS)
        descr[USERNAME] = descr.pop(RespC.UserInfo.NAME)
        descr[BLOG_COUNT] = len(descr.pop(RespC.UserInfo.BLOGS))
        descr.move_to_end(USERNAME, last=False)
        return descr


class UserBlogDescription(Description):

    _keys = [RespC.UserBlogInfo.TITLE,
             RespC.UserBlogInfo.NAME,
             RespC.UserBlogInfo.URL,
             RespC.UserBlogInfo.DESCRIPTION,
             RespC.UserBlogInfo.TYPE,
             RespC.UserBlogInfo.ADMIN,
             RespC.UserBlogInfo.POSTS,
             RespC.UserBlogInfo.DRAFTS,
             RespC.UserBlogInfo.QUEUE,
             RespC.UserBlogInfo.TOTAL_POSTS,
             RespC.UserBlogInfo.LIKES,
             RespC.UserBlogInfo.SHARE_LIKES,
             RespC.UserBlogInfo.FOLLOWERS,
             RespC.UserBlogInfo.MESSAGES,
             RespC.UserBlogInfo.MESSAGING_ALLOW_FOLLOWS_ONLY,
             RespC.UserBlogInfo.ASK,
             RespC.UserBlogInfo.CAN_MESSAGE,
             RespC.UserBlogInfo.CAN_SUBSCRIBE,
             RespC.UserBlogInfo.CAN_SEND_FAN_MAIL,
             RespC.UserBlogInfo.NOTIFICATION_SETTINGS,
             RespC.UserBlogInfo.IS_ADULT,
             RespC.UserBlogInfo.IS_NSFW]

    @property
    def links(self):
        links = []
        blog_name = self._raw[RespC.UserBlogInfo.NAME]
        posts = flask.url_for(Rc.Subdomains.POSTS_PAGE, subdomain=blog_name)
        links.append(BuildHtmlUtils.to_href(posts, 'posts'))
        likes = flask.url_for(Rc.Subdomains.LIKES, subdomain=blog_name)
        links.append(BuildHtmlUtils.to_href(likes, 'likes'))
        if self._raw.get(RespC.UserBlogInfo.FOLLOWERS, 0) > 0:
            url = flask.url_for(Rc.Subdomains.FOLLOWERS, subdomain=blog_name)
            links.append(BuildHtmlUtils.to_href(url, 'followers'))
        return links

    @classmethod
    def format_description(cls, descr):
        descr[BLOG_NAME] = descr.pop(RespC.UserBlogInfo.NAME)
        descr[RespC.UserBlogInfo.URL] = BuildHtmlUtils.to_href(descr[RespC.UserBlogInfo.URL])
        descr.move_to_end(BLOG_NAME, last=False)
        return descr
