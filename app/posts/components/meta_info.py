from constants import responses as RespC


class MetaInfo(dict):

    """
    General information about the post
    keys:
        blog -> the name of blog the post is on
        id -> the id of the post
        reblog_key -> reblog key of the post
        liked -> whether or not the user has liked the post
        date -> date that the post was posted
        note_count -> number of notes
    """

    def __init__(self, json):
        super(MetaInfo, self).__init__(blog=json.get(RespC.Post.BLOG_NAME),
                                       id=json.get(RespC.Post.ID),
                                       reblog_key=json.get(RespC.Post.REBLOG_KEY),
                                       liked=json.get(RespC.Post.LIKED),
                                       date=json.get(RespC.Post.DATE),
                                       note_count=json.get(RespC.Post.NOTE_COUNT))
