import re
from flask import url_for
from constants import routes as Rc


class TumblrDomainUtils:

    @staticmethod
    def get_subdomain(tumblr_domain: str) -> str:
        pattern = re.compile('^(http://|https://|)(.*)\.tumblr\.com')
        subdomain = pattern.match(tumblr_domain).group(2)
        return subdomain

    @classmethod
    def to_noneblr(cls, tumblr_domain: str, route=Rc.Subdomains.POSTS_PAGE, **kwargs) -> str:
        try:
            subdomain = cls.get_subdomain(tumblr_domain)
            converted = url_for(route, subdomain=subdomain, **kwargs)
        except (TypeError, AttributeError):
            converted = tumblr_domain
        return converted
