from .post import *
from constants import posts as Pc, responses as RespC


class Factory:
    """
    given a posts json object, determine the post type and create the corresponding post object
    """
    @classmethod
    def create(cls, json):
        """
        create a bost from a json object. all components are the same between posts except the body.
        Use the class method create body to create the relevant body type.
        """
        post_type = json[RespC.Post.TYPE]
        meta_info = MetaInfo(json)
        source = Source(json)
        body = cls.create_body(post_type, json)
        if RespC.Post.NOTES in json:
            notes = Notes(json[RespC.Post.NOTES])
        else:
            notes = None
        return Post(post_type, body, meta_info, source, notes)

    @staticmethod
    def create_body(post_type: str, json: dict) -> Body:
        post_obj = TextPost
        if post_type == Pc.Types.PHOTO:
            post_obj = PhotoPost
        elif post_type == Pc.Types.VIDEO:
            post_obj = VideoPost
        elif post_type == Pc.Types.QUOTE:
            post_obj = QuotePost
        elif post_type == Pc.Types.LINK:
            post_obj = LinkPost
        elif post_type == Pc.Types.ANSWER:
            post_obj = AnswerPost
        elif post_type == Pc.Types.AUDIO:
            post_obj = AudioPost
        elif post_obj == Pc.Types.CHAT:
            post_obj = ChatPost
        return post_obj(json)
