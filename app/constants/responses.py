class Response:
    POSTS = 'posts'
    BLOG_INFO = 'blog'
    BLOGS_INFO = 'blogs'
    USERS = 'users'
    TOTAL_POSTS = 'total_posts'
    TOTAL_BLOGS = 'total_blogs'
    TOTAL_USERS = 'total_users'
    LIKED_COUNT = 'liked_count'
    LIKED_POSTS = 'liked_posts'
    POST_TYPE = 'post_type'


class UserInfo:
    NAME = 'name'
    USER = 'user'
    BLOGS = 'blogs'
    DEFAULT_POST_FORMAT = 'default_post_format'
    LIKES = 'likes'
    FOLLOWING = 'following'


class UserBlogInfo:
    IS_GROUP_CHANNEL = 'is_group_channel'
    CAN_MESSAGE = 'can_message'
    PLACEMENT_ID = 'placement_id'
    LIKES = 'likes'
    ASK_ANON = 'ask_anon'
    FACEBOOK = 'facebook'
    RANDOM_NAME = 'random_name'
    FOLLOWERS = 'followers'
    MESSAGING_ALLOW_FOLLOWS_ONLY = 'messaging_allow_follows_only'
    SECONDS_SINCE_LAST_ACTIVITY = 'seconds_since_last_activity'
    TYPE = 'type'
    SHARE_FOLLOWING = 'share_following'
    POSTS = 'posts'
    UUID = 'uuid'
    ASK_PAGE_TITLE = 'ask_page_title'
    IS_PRIVATE_CHANNEL = 'is_private_channel'
    PRIMARY = 'primary'
    NOTIFICATION_SETTINGS = 'notification_settings'
    IS_NSFW = 'is_nsfw'
    TWITTER_ENABLED = 'twitter_enabled'
    THEME = 'theme'
    NAME = 'name'
    ADMIN = 'admin'
    ASK = 'ask'
    DESCRIPTION = 'description'
    URL = 'url'
    TITLE = 'title'
    IS_ADULT = 'is_adult'
    SHARE_LIKES = 'share_likes'
    FACEBOOK_OPENGRAPH_ENABLED = 'facebook_opengraph_enabled'
    FOLLOWED = 'followed'
    DRAFTS = 'drafts'
    CAN_SEND_FAN_MAIL = 'can_send_fan_mail'
    SHOW_AUTHOR_AVATAR = 'show_author_avatar'
    MESSAGES = 'messages'
    UPDATED = 'updated'
    TWITTER_SEND = 'twitter_send'
    NOTIFICATIONS = 'notifications'
    REPLY_CONDITIONS = 'reply_conditions'
    SUBSCRIBED = 'subscribed'
    CAN_SUBSCRIBE = 'can_subscribe'
    TWEET = 'tweet'
    QUEUE = 'queue'
    IS_BLOCKED_FROM_PRIMARY = 'is_blocked_from_primary'
    TOTAL_POSTS = 'total_posts'


class Error:
    META = 'meta'
    MESSAGE = 'msg'


class BlogInfo:
    NAME = 'name'
    TITLE = 'title'
    ASK = 'ask'
    ASK_ANON = 'ask_anon'
    CAN_SUBSCRIBE = 'can_subscribe'
    DESCRIPTION = 'description'
    IS_ADULT = 'is_adult'
    IS_NSFW = 'is_nsfw'
    POSTS = 'posts'
    REPLY_CONDITIONS = 'reply_conditions'
    SHARE_LIKES = 'share_likes'
    SUBSCRIBED = 'subscribed'
    TOTAL_POSTS = 'total_posts'
    UPDATED = 'updated'
    URL = 'url'
    LIKES = 'likes'
    CAN_MESSAGE = 'can_message'
    THEME = 'theme'
    KEY = 'key'
    CAN_BE_FOLLOWED = 'can_be_followed'
    PLACEMENT_ID = 'placement_id'
    SHARE_FOLLOWING = 'share_following'
    UUID = 'uuid'
    PRIMARY = 'primary'
    FOLLOWED = 'followed'


class Post:
    BLOG_NAME = 'blog_name'
    ID = 'id'
    REBLOG_KEY = 'reblog_key'
    REBLOGGED_FROM_UUID = 'reblogged_from_uuid'
    REBLOGGED_FROM_NAME = 'reblogged_from_name'
    REBLOGGED_FROM_URL = 'reblogged_from_url'
    SOURCE_TITLE = 'source_title'
    SOURCE_URL = 'source_url'
    LIKED = 'liked'
    DATE = 'date'
    TYPE = 'type'
    NOTES = 'notes'
    NOTE_COUNT = 'note_count'


class TextPost:
    TEXT = 'body'
    TITLE = 'title'


class QuotePost:
    QUOTE = 'text'
    COMMENT = 'comment'
    REBLOG = 'reblog'


class LinkPost:
    LINK = 'url'
    TITLE = 'title'


class AnswerPost:
    ASKER = 'asking_name'
    ASKER_URL = 'asking_url'
    QUESTION = 'question'
    ANSWER = 'answer'


class VideoPost:
    PLAYER = 'player'
    EMBED_CODE = 'embed_code'
    MUTED = 'muted'
    CONTROLS = 'controls'
    CAPTION = 'caption'


class AudioPost:
    PLAYER = 'embed'
    CAPTION = 'caption'


class PhotoPost:
    PHOTOS = 'photos'
    ORIGINAL_SIZE = 'original_size'
    URL = 'url'
    ALT_SIZES = 'alt_sizes'
    WIDTH = 'width'
    CAPTION = 'caption'


class ChatPost:
    CONVERSATION = 'body'
