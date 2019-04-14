from utils.url_utils import TumblrDomainUtils
from bs4 import BeautifulSoup
from utils.html_utils import ParseHtmlUtils, BuildHtmlUtils
from constants import responses as RespC
import bleach

MAX_PHOTO_WIDTH = 3000


class Body(dict):

    def __init__(self, json: dict):
        super(Body, self).__init__(self.construct(json))

    @classmethod
    def construct(cls, json):
        raise NotImplementedError


class TextPost(Body):

    @classmethod
    def construct(cls, json):
        return {'text': ParseHtmlUtils.convert_tumblr_references(json[RespC.TextPost.TEXT]),
                'title': json[RespC.TextPost.TITLE]}


class QuotePost(Body):

    @classmethod
    def construct(cls, json):
        comment = json[RespC.QuotePost.REBLOG].get(RespC.QuotePost.COMMENT)
        if comment:
            comment = ParseHtmlUtils.convert_tumblr_references(comment)
        return {'quote': json[RespC.QuotePost.QUOTE],
                'comment': comment}


class LinkPost(Body):

    @classmethod
    def construct(cls, json):
        return {'link': json[RespC.LinkPost.LINK],
                'title': json[RespC.LinkPost.TITLE]}


class AnswerPost(Body):

    @classmethod
    def construct(cls, json):
        return {'asker': json[RespC.AnswerPost.ASKER],
                'asker_href': TumblrDomainUtils.to_noneblr(json[RespC.AnswerPost.ASKER_URL]),
                'question': json[RespC.AnswerPost.QUESTION],
                'answer': json[RespC.AnswerPost.ANSWER]}


class VideoPost(Body):

    @classmethod
    def construct(cls, json):
        caption = json.get(RespC.VideoPost.CAPTION)
        if caption:
            caption = ParseHtmlUtils.convert_tumblr_references(caption)
        return {'player': cls.build_player(json[RespC.VideoPost.PLAYER][-1]),
                'caption': BuildHtmlUtils.bleach(caption)}

    @staticmethod
    def build_player(player):
        embed = player.get(RespC.VideoPost.EMBED_CODE)
        if embed:
            embed = BeautifulSoup(player[RespC.VideoPost.EMBED_CODE], 'html.parser')
            if embed.video and RespC.VideoPost.MUTED in embed.video.attrs:
                del embed.video[RespC.VideoPost.MUTED]
            if embed.source:
                embed.video.attrs.update(embed.source.attrs)
                embed.video.attrs[RespC.VideoPost.CONTROLS] = ''
                embed.source.extract()
                embed = embed
        return embed


class AudioPost(Body):

    @classmethod
    def construct(cls, json):
        caption = json.get(RespC.AudioPost.CAPTION)
        if caption:
            caption = ParseHtmlUtils.convert_tumblr_references(caption)
        return {'player': json[RespC.AudioPost.PLAYER],
                'caption': BuildHtmlUtils.bleach(caption)}


class PhotoPost(Body):

    @classmethod
    def construct(cls, json):
        caption = json.get(RespC.PhotoPost.CAPTION)
        if caption:
            caption = ParseHtmlUtils.convert_tumblr_references(caption)
        photos, width = cls.build_photos(json[RespC.PhotoPost.PHOTOS])
        return {'photos': photos,
                'width': max(width),
                'caption': BuildHtmlUtils.bleach(caption)}

    @staticmethod
    def build_photos(photo_json):
        photos = []
        widths = []
        for photo in photo_json:
            href = photo[RespC.PhotoPost.ORIGINAL_SIZE][RespC.PhotoPost.URL]
            width = photo[RespC.PhotoPost.ORIGINAL_SIZE][RespC.PhotoPost.WIDTH]
            source = href
            for alt_source in photo[RespC.PhotoPost.ALT_SIZES]:
                if alt_source[RespC.PhotoPost.WIDTH] < MAX_PHOTO_WIDTH:
                    source = alt_source[RespC.PhotoPost.URL]
                    width = alt_source[RespC.PhotoPost.WIDTH]
                    break
            photos.append({'href': href, 'source': source})
            widths.append(width)
        return photos, widths


class ChatPost(Body):

    @classmethod
    def construct(cls, json):
        return {'conversation': cls.build_conversation(BeautifulSoup(json[RespC.ChatPost.CONVERSATION], 'html.parser'))}

    @staticmethod
    def build_conversation(body):
        if body.string:
            conversation = body.string.extract()
        else:
            conversation = body.text
        return conversation.split('\n')
