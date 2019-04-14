from utils.url_utils import TumblrDomainUtils
from bs4 import BeautifulSoup
import bleach

bleach.ALLOWED_TAGS.extend(['p', 'br', 'small', 'hr', 'figure', 'img', 'h2', 'span', 'iframe', 'font'])


class ParseHtmlUtils:

    @staticmethod
    def convert_tumblr_references(html, parser='html.parser'):
        parsed = BeautifulSoup(html, parser)
        for tumblr_blog in parsed.find_all('a', class_='tumblr_blog'):
            href = tumblr_blog['href']
            if 'tumblr.com' in href:
                tumblr_blog['href'] = TumblrDomainUtils.to_noneblr(href)
        return parsed


class BuildHtmlUtils:

    @staticmethod
    def bleach(html):
        return bleach.clean(html)

    @staticmethod
    def to_href(href, display=None):
        soup = BeautifulSoup()
        a_tag = soup.new_tag('a')
        a_tag['href'] = href
        if not display:
            display = href
        a_tag.append(display)
        return a_tag

    @classmethod
    def list_to_html(cls, raw_list, parent="p"):
        soup = BeautifulSoup()
        parent = soup.new_tag(parent)
        for item in raw_list:
            if isinstance(item, list):
                parent.append(cls.list_to_html(item))
            elif isinstance(item, dict):
                parent.append(cls.dict_to_html(item))
            else:
                li = soup.new_tag("li")
                li.append(item)
                parent.append(li)
        return parent.prettify(formatter=None)

    @classmethod
    def dict_to_html(cls, raw_dict, parent="ul"):
        soup = BeautifulSoup()
        parent = soup.new_tag(parent)
        for key, val in raw_dict.items():
            li = soup.new_tag("li")
            if isinstance(val, list):
                li.append("{}:".format(key))
                li.append(cls.list_to_html(val, "div"))
            elif isinstance(val, dict):
                li.append("{}:".format(key))
                li.append(cls.dict_to_html(val))
            else:
                li.append("{}: {}".format(key, val))
            parent.append(li)
        return parent.prettify(formatter=None)
