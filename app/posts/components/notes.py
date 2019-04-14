from flask import url_for
from constants import routes as Rc
from constants import responses as RespC


class Notes(list):
    """
    List of Note dictionaries.
    """

    def __init__(self, json: list):
        super(Notes, self).__init__([Note(x) for x in json])


class Note(dict):
    """
    dictionary of form:
        type -> type of note ie like or reblog
        blog_name -> name of the blog that the note is from
        blog_href -> href to the blog that the note is from
    """
    def __init__(self, json):
        super(Note, self).__init__(type=json[RespC.Post.TYPE],
                                   blog_name=json[RespC.Post.BLOG_NAME],
                                   blog_href=url_for(Rc.Subdomains.POSTS_PAGE, subdomain=json[RespC.Post.BLOG_NAME]))
