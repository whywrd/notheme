import flask
from constants import routes as Rc, responses as RespC, oauth as OAuthC, session as SeshC, forms as FormC, \
    style as StyleC, requests as ReqC
from pages.components import navigation as nav
from tumblr_api_handler import request_handlers as request_handlers
from tumblr_api_handler.params import blog_method_params, user_method_params, tagged_method_params
from tumblr_api_handler.requests import blog_methods, user_methods, tagged_methods
from exceptions.requests import InvalidUsage
from pages import post_pages, info_pages, likes_page
from rauth import OAuth1Service
from utils import url_utils
import urllib.parse
import flask_mobility
from reverse_proxy_wrapper import ReverseProxied

app = flask.Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)
app.config.from_object('config')
flask_mobility.Mobility(app)

oauth_service = OAuth1Service(name='tumblr',
                              consumer_key=app.config[OAuthC.CONSUMER_KEY],
                              consumer_secret=app.config[OAuthC.SECRET_KEY],
                              request_token_url=OAuthC.REQUEST_TOKEN_URL,
                              authorize_url=OAuthC.AUTHORIZE_URL,
                              access_token_url=OAuthC.ACCESS_TOKEN_URL)

# CONSTANTS
POST_LIMIT = 10
BLOG_LIMIT = 10
FOLLOWING_LIMIT = 10
FOLLOWERS_LIMIT = 10
REDIRECT = 'r'


# BEFORE REQUEST

@app.before_request
def set_request_handler():
    if not flask.session.get(SeshC.LOGGED_IN, False):
            flask.g.request_handler = request_handlers.PublicRequestHandler()
    else:
        flask.g.request_handler = request_handlers.OauthRequestHandler(app.config[OAuthC.CONSUMER_KEY],
                                                                       app.config[OAuthC.SECRET_KEY],
                                                                       flask.session[SeshC.OAUTH_TOKEN])
    if not flask.request.MOBILE:
        flask.g.style = StyleC.DESKTOP
    else:
        flask.g.style = StyleC.MOBILE

# ROUTES


@app.route('/')
def index():
    return flask.render_template('pages/index.html')


@app.route('/search', methods=['POST'])
def search():
    search_value = flask.request.form[FormC.Search.VALUE].strip()
    if search_value.find('#') == 0:
        tag = urllib.parse.quote_plus(search_value[1:])
        redirect = flask.url_for(Rc.Tagged.TAGGED, **{ReqC.Tagged.TAG: tag})
    else:
        subdomain = urllib.parse.quote_plus(search_value)
        try:
            subdomain = url_utils.TumblrDomainUtils.get_subdomain(search_value)
        except AttributeError:
            pass
        redirect = flask.url_for(Rc.Subdomains.POSTS_PAGE, subdomain=subdomain)
    return flask.redirect(redirect)


@app.route('/', subdomain='<subdomain>')
@app.route('/<post_type>', subdomain='<subdomain>')
@app.route('/page/<int:page_number>', subdomain='<subdomain>')
@app.route('/<post_type>/page/<int:page_number>', subdomain='<subdomain>')
def subdomain_posts(subdomain, post_type='', page_number=1):
    params = blog_method_params.PostsParams()
    params.blog_identifier = subdomain
    params.api_key = app.config[OAuthC.CONSUMER_KEY]
    params.post_type = post_type
    params.limit = POST_LIMIT
    params.offset = (page_number - 1) * POST_LIMIT
    params.reblog_info = True
    params.notes_info = False
    request = blog_methods.PostsQuery(params)
    resp = flask.g.request_handler.query(request)
    resp = resp[request_handlers.JSON]
    page = post_pages.SubdomainPostPage(resp, post_type=post_type)
    navigation = nav.Navigation(page_number, POST_LIMIT, resp[RespC.Response.TOTAL_POSTS],
                                Rc.Subdomains.POSTS_PAGE, post_type=post_type, subdomain=subdomain)

    return flask.render_template('pages/post_pages/subdomain_posts.html', page=page, navigation=navigation)


@app.route('/post_type', subdomain='<subdomain>', methods=['POST'])
def subdomain_type_posts(subdomain):
    post_type = flask.request.form.get('post_type')
    url = flask.url_for('subdomain_posts', subdomain=subdomain, post_type=post_type, _external=True)
    return flask.redirect(url)


@app.route('/post/<int:post_id>/', subdomain='<subdomain>')
@app.route('/post/<int:post_id>/<post_name>', subdomain='<subdomain>')
def subdomain_post(subdomain, post_id, post_name=''):
    params = blog_method_params.PostsParams()
    params.blog_identifier = subdomain
    params.api_key = app.config[OAuthC.CONSUMER_KEY]
    params.post_id = post_id
    params.reblog_info = True
    params.notes_info = True
    request = blog_methods.PostsQuery(params)
    resp = flask.g.request_handler.query(request)
    resp = resp[request_handlers.JSON]

    page = post_pages.SubdomainPostPage(resp)

    return flask.render_template('pages/post_pages/subdomain_post.html', page=page, navigation=None)


@app.route('/info', subdomain='<subdomain>')
def subdomain_info(subdomain):
    params = blog_method_params.InfoParams()
    params.blog_identifier = subdomain
    params.api_key = app.config[OAuthC.CONSUMER_KEY]
    request = blog_methods.InfoQuery(params)
    resp = flask.g.request_handler.query(request)
    resp = resp[request_handlers.JSON]

    page = info_pages.SubdomainInfoPage(resp)

    return flask.render_template('pages/info_pages/subdomain_info.html', page=page)


@app.route('/info')
def user_info():
    if not flask.session.get(SeshC.LOGGED_IN, False):
        return flask.redirect(flask.url_for(Rc.Authorization.AUTHORIZE))
    params = user_method_params.InfoParams()
    request = user_methods.InfoQuery(params)
    resp = flask.g.request_handler.query(request)
    resp = resp[request_handlers.JSON]

    page = info_pages.UserInfoPage(resp)
    return flask.render_template('pages/info_pages/user_info.html', page=page)


@app.route('/likes', subdomain='<subdomain>')
@app.route('/likes/page/<int:page_number>', subdomain='<subdomain>')
def subdomain_likes(subdomain, page_number=1):
    info_params = blog_method_params.InfoParams()
    info_params.blog_identifier = subdomain
    info_params.api_key = app.config[OAuthC.CONSUMER_KEY]
    info_request = blog_methods.InfoQuery(info_params)
    info_resp = flask.g.request_handler.query(info_request)
    info_resp = info_resp[request_handlers.JSON]

    likes_params = blog_method_params.LikesParams()
    likes_params.blog_identifier = subdomain
    likes_params.api_key = app.config[OAuthC.CONSUMER_KEY]
    likes_params.limit = POST_LIMIT
    likes_params.offset = (page_number - 1) * POST_LIMIT
    likes_params.reblog_info = True
    likes_params.notes_info = False
    likes_request = blog_methods.LikesQuery(likes_params)
    likes_resp = flask.g.request_handler.query(likes_request)
    likes_resp = likes_resp[request_handlers.JSON]

    page = likes_page.LikesPage(info_resp, likes_resp)
    navigation = nav.Navigation(page_number, POST_LIMIT, likes_resp[RespC.Response.LIKED_COUNT],
                                Rc.Subdomains.LIKES, subdomain=subdomain)

    return flask.render_template('pages/post_pages/subdomain_posts.html', page=page, navigation=navigation)


@app.route('/dashboard')
@app.route('/dashboard/<post_type>')
@app.route('/dashboard/page/<int:page_number>')
@app.route('/dashboard/<post_type>/page/<int:page_number>')
def dashboard(post_type=None, page_number=1):
    if not flask.session.get(SeshC.LOGGED_IN, False):
        return flask.redirect(flask.url_for(Rc.Authorization.AUTHORIZE))

    params = user_method_params.DashboardParams()
    params.post_type = post_type
    params.limit = POST_LIMIT
    params.offset = (page_number - 1) * POST_LIMIT
    params.reblog_info = True
    params.notes_info = False
    request = user_methods.DashboardQuery(params)
    resp = flask.g.request_handler.query(request)
    resp = resp[request_handlers.JSON]

    page = post_pages.DashboardPostPage(resp)
    navigation = nav.Navigation(page_number, POST_LIMIT, None, Rc.User.DASHBOARD, post_type=post_type)

    return flask.render_template('pages/post_pages/dashboard.html', page=page, navigation=navigation)


@app.route('/following')
@app.route('/following/page/<int:page_number>')
def user_following(page_number=1):
    if not flask.session.get(SeshC.LOGGED_IN, False):
        return flask.redirect(flask.url_for(Rc.Authorization.AUTHORIZE))

    params = user_method_params.FollowingParams()
    params.limit = FOLLOWING_LIMIT
    params.offset = (page_number - 1) * FOLLOWING_LIMIT
    request = user_methods.FollowingQuery(params)
    resp = flask.g.request_handler.query(request)
    resp = resp[request_handlers.JSON]

    page = info_pages.FollowingPage(resp)
    navigation = nav.Navigation(page_number, FOLLOWING_LIMIT, resp[RespC.Response.TOTAL_BLOGS], Rc.User.FOLLOWING)
    return flask.render_template('pages/info_pages/following.html', page=page, navigation=navigation)


@app.route('/followers', subdomain='<subdomain>')
@app.route('/followers/page/<int:page_number>', subdomain='<subdomain>')
def followers(subdomain, page_number=1):
    if not flask.session.get(SeshC.LOGGED_IN, False):
        return flask.redirect(flask.url_for(Rc.Authorization.AUTHORIZE))

    params = blog_method_params.FollowersParams()
    params.blog_identifier = subdomain
    params.limit = FOLLOWERS_LIMIT
    params.offset = (page_number - 1) * FOLLOWERS_LIMIT
    request = blog_methods.FollowersQuery(params)
    resp = flask.g.request_handler.query(request)
    resp = resp[request_handlers.JSON]

    page = info_pages.FollowersPage(resp)
    navigation = nav.Navigation(page_number, FOLLOWERS_LIMIT, resp[RespC.Response.TOTAL_USERS], Rc.Subdomains.FOLLOWERS,
                                subdomain=subdomain)
    return flask.render_template('pages/info_pages/followers.html', page=page, navigation=navigation)


@app.route('/follow/<blog_name>')
def follow(blog_name):
    if not flask.session.get(SeshC.LOGGED_IN, False):
        return flask.redirect(flask.url_for(Rc.Authorization.AUTHORIZE))
    r = flask.request.args.get(REDIRECT, flask.url_for(Rc.User.DASHBOARD))
    params = user_method_params.FollowParams()
    params.url = blog_name
    request = user_methods.FollowQuery(params)
    resp = flask.g.request_handler.query(request)
    if resp[request_handlers.STATUS_CODE] not in [200, 201]:
        construct_invalid_usage_exception(resp)
    return flask.redirect(r)


@app.route('/unfollow/<blog_name>')
def unfollow(blog_name):
    if not flask.session.get(SeshC.LOGGED_IN, False):
        return flask.redirect(flask.url_for(Rc.Authorization.AUTHORIZE))
    r = flask.request.args.get(REDIRECT, flask.url_for(Rc.User.DASHBOARD))
    params = user_method_params.UnfollowParams()
    params.url = blog_name
    request = user_methods.UnfollowQuery(params)
    resp = flask.g.request_handler.query(request)
    if resp[request_handlers.STATUS_CODE] not in [200, 201]:
        construct_invalid_usage_exception(resp)
    return flask.redirect(r)


@app.route('/like', methods=['POST'])
@app.route('/like', subdomain='<subdomain>', methods=['POST'])
def like(subdomain=None):
    params = user_method_params.LikeParams()
    params.post_id = flask.request.form[FormC.Like.POST_ID]
    params.reblog_key = flask.request.form[FormC.Like.REBLOG_KEY]
    request = user_methods.LikeQuery(params)
    resp = flask.g.request_handler.query(request)
    if resp[request_handlers.STATUS_CODE] != 200:
        raise construct_invalid_usage_exception(resp)
    return flask.jsonify({request_handlers.RESPONSE: resp[request_handlers.STATUS_CODE]})


@app.route('/unlike', methods=['POST'])
@app.route('/unlike', subdomain='<subdomain>', methods=['POST'])
def unlike(subdomain=None):
    params = user_method_params.UnlikeParams()
    params.post_id = flask.request.form[FormC.Like.POST_ID]
    params.reblog_key = flask.request.form[FormC.Like.REBLOG_KEY]
    request = user_methods.UnlikeQuery(params)
    resp = flask.g.request_handler.query(request)
    if resp[request_handlers.STATUS_CODE] != 200:
        raise construct_invalid_usage_exception(resp)
    return flask.jsonify({request_handlers.RESPONSE: resp[request_handlers.STATUS_CODE]})


@app.route('/reblog/<int:post_id>', subdomain='<subdomain>')
def reblog(subdomain, post_id):
    if not flask.session.get(SeshC.LOGGED_IN, False):
        return flask.redirect(flask.url_for(Rc.Authorization.AUTHORIZE))
    post_params = blog_method_params.PostsParams()
    post_params.blog_identifier = subdomain
    post_params.api_key = app.config[OAuthC.CONSUMER_KEY]
    post_params.post_id = post_id
    post_params.reblog_info = True
    post_params.notes_info = False
    post_request = blog_methods.PostsQuery(post_params)
    post_resp = flask.g.request_handler.query(post_request)
    post_resp = post_resp[request_handlers.JSON]

    user_info_params = user_method_params.InfoParams()
    user_info_request = user_methods.InfoQuery(user_info_params)
    user_info_resp = flask.g.request_handler.query(user_info_request)
    user_info_resp = user_info_resp[request_handlers.JSON]

    page = post_pages.ReblogPostPage(user_info_resp, post_resp)

    flask.session[SeshC.REDIRECT] = flask.request.args.get(SeshC.REDIRECT)

    return flask.render_template('pages/post_pages/reblog.html', page=page)


@app.route('/reblog/', subdomain='<subdomain>', methods=['POST'])
def reblog_form(subdomain):
    r = flask.session.pop(REDIRECT, flask.url_for(Rc.User.DASHBOARD, _external=True))
    params = blog_method_params.ReblogPostParams()
    params.post_id = flask.request.form.get(FormC.Reblog.POST_ID)
    params.reblog_key = flask.request.form.get(FormC.Reblog.REBLOG_KEY)
    params.comment = flask.request.form.get(FormC.Reblog.COMMENT)
    params.native_inline_images = flask.request.form.get(FormC.Reblog.NATIVE_INLINE_IMAGES, True)
    for blog in flask.request.form.getlist(FormC.Reblog.BLOG_IDENTIFIER):
        params.blog_identifier = blog
        request = blog_methods.ReblogPostQuery(params)
        resp = flask.g.request_handler.query(request)
        if resp[request_handlers.STATUS_CODE] not in [200, 201]:
            raise construct_invalid_usage_exception(resp)
    return flask.redirect(r)


@app.route('/tagged')
def tagged():
    params = tagged_method_params.TaggedParams()
    params.api_key = app.config[OAuthC.CONSUMER_KEY]
    params.tag = flask.request.args.get(ReqC.Tagged.TAG)
    params.before = flask.request.args.get(ReqC.Tagged.BEFORE)
    params.filter_nsfw = 'false'
    request = tagged_methods.TaggedQuery(params)
    resp = flask.g.request_handler.query(request)
    resp = resp[request_handlers.JSON]
    resp = {RespC.Response.POSTS: resp}

    page = post_pages.TaggedPostPage(resp)

    return flask.render_template('pages/post_pages/base.html', page=page)


@app.route('/delete/<post_id>', subdomain='<blog_identifier>')
def delete_post(blog_identifier, post_id):
    r = flask.request.args.get(REDIRECT, flask.url_for(Rc.User.DASHBOARD))
    params = blog_method_params.DeletePostParams()
    params.blog_identifier = blog_identifier
    params.post_id = post_id
    request = blog_methods.DeletePostQuery(params)
    resp = flask.g.request_handler.query(request)

    if resp[request_handlers.STATUS_CODE] not in [200, 201]:
        raise construct_invalid_usage_exception(resp)
    return flask.redirect(r)


@app.route('/authorize')
def authorize():
    flask.session[SeshC.REDIRECT] = flask.request.args.get(SeshC.REDIRECT)
    token = oauth_service.get_request_token()
    auth_url = oauth_service.get_authorize_url(token[0])
    flask.session[OAuthC.OAUTH_TOKEN] = token
    return flask.redirect(auth_url)


@app.route('/callback')
def oauth_callback():
    oauth_token = flask.session[OAuthC.OAUTH_TOKEN]
    oauth_verifier = flask.request.args.get(OAuthC.OAUTH_VERIFIER)
    if oauth_verifier:
        data = {OAuthC.OAUTH_VERIFIER: oauth_verifier}
        token = oauth_service.get_access_token(request_token=oauth_token[0],
                                               request_token_secret=oauth_token[1],
                                               data=data)

        flask.session[SeshC.LOGGED_IN] = True
        flask.session[SeshC.OAUTH_TOKEN] = token

        flask.g.request_handler = request_handlers.OauthRequestHandler(app.config[OAuthC.CONSUMER_KEY],
                                                                       app.config[OAuthC.SECRET_KEY],
                                                                       token)

        params = user_method_params.InfoParams()
        request = user_methods.InfoQuery(params)
        user_info = flask.g.request_handler.query(request)[request_handlers.JSON]

        user_blog_names = \
            [blog[RespC.UserInfo.NAME] for blog in user_info[RespC.UserInfo.USER][RespC.UserInfo.BLOGS]]
        flask.session[SeshC.USER_BLOGS] = user_blog_names

    r = flask.session.pop(SeshC.REDIRECT)
    redirect = r
    if not redirect:
        redirect = flask.url_for(Rc.User.DASHBOARD)
    return flask.redirect(redirect)


@app.route('/logout')
def logout():
    flask.session.pop(SeshC.OAUTH_TOKEN)
    flask.session[SeshC.LOGGED_IN] = False
    r = flask.request.args.get(SeshC.REDIRECT)
    return flask.redirect(r)


@app.route('/favicon.ico', subdomain='<subdomain>')
def favicon(subdomain):
    return subdomain


def construct_invalid_usage_exception(resp):
    exception = InvalidUsage()
    exception.description = resp[request_handlers.JSON][RespC.Error.META][RespC.Error.MESSAGE]
    exception.code = resp[request_handlers.STATUS_CODE]
    return exception


def test():
    app.config.update(SERVER_NAME=app.config.get('SERVER_NAME'))
    app.run()


def main():
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
