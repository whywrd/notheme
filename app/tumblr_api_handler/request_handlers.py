import oauth2
from exceptions.requests import InvalidUsage
from simplejson.scanner import JSONDecodeError
from urllib.parse import urlencode
import requests
from tumblr_api_handler.requests import requests as r
from utils.url_utils import TumblrDomainUtils
import json

STATUS_CODE = 'status_code'
OAUTH_STATUS = 'status'
JSON = 'json'
RESPONSE = 'response'
ERRORS = 'errors'
ERROR_DETAIL = 'detail'


class RequestHandler:

    """
    abstract handler class.
    """

    def create_session(self):
        raise NotImplementedError

    def get(self, url):
        raise NotImplementedError

    def post(self, url, data):
        raise NotImplementedError

    @staticmethod
    def process_resp(resp):
        raise NotImplementedError

    def query(self, query):
        if isinstance(query, r.GETRequest):
            resp = self.get(query.url)
        elif isinstance(query, r.POSTRequest):
            resp = self.post(query.url, query.data)
        else:
            raise NotImplementedError
        return resp


class OauthRequestHandler(RequestHandler):

    def __init__(self, consumer_key, secret_key, token):
        self._consumer_key = consumer_key
        self._secret_key = secret_key
        self._token = token
        self.session = self.create_session()

    def create_session(self):
        consumer = oauth2.Consumer(self._consumer_key, self._secret_key)
        token = oauth2.Token(*self._token)
        return oauth2.Client(consumer, token)

    def get(self, url):
        return self.process_resp(self.session.request(url))

    def post(self, url, data):
        return self.process_resp(self.session.request(url, 'POST', urlencode(data)))

    @staticmethod
    def process_resp(resp):
        return {STATUS_CODE: int(resp[0][OAUTH_STATUS]),
                JSON: json.loads(resp[1].decode('UTF-8'))[RESPONSE]}


class PublicRequestHandler(RequestHandler):

    def __init__(self):
        self.session = self.create_session()

    def create_session(self):
        return requests.Session()

    def get(self, url):
        return self.process_resp(self.session.get(url))

    def post(self, url, data):
        return self.process_resp(self.session.post(url, data))

    @staticmethod
    def process_resp(resp):
        try:
            json_body = resp.json()
            if not resp.ok:
                raise InvalidUsage(code=resp.status_code,
                                   description='The tumbler api says: {}'.format(json_body[ERRORS][0][ERROR_DETAIL]),
                                   subdomain=TumblrDomainUtils.get_subdomain(resp.url))
        except JSONDecodeError:
            raise InvalidUsage(code=500)
        return {STATUS_CODE: resp.status_code, JSON: json_body[RESPONSE]}
