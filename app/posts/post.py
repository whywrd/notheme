from posts.components import *


class Post:
    """
    A generic post object. Composed of notes, source info, post info and a body.
    """
    def __init__(self, post_type: str, body: Body, meta_info: MetaInfo, source: Source, notes: Notes):
        self.type = post_type
        self.body = body
        self.meta_info = meta_info
        self.source = source
        self.notes = notes
