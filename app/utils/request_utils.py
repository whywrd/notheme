import oauth2 as oauth
import requests
import json
from urllib.parse import urlencode
from simplejson.scanner import JSONDecodeError
from components.exceptions import InvalidUsage


def oauth_request(url: str, oauth_client: oauth.Client, method: str ='GET', data: dict=None):
    """
    Method to request url given an authenticated oauth client
    """
    if method == 'GET':
        resp = oauth_client.request(url)
    else:
        resp = oauth_client.request(url, 'POST', urlencode(data))
    status_code = int(resp[0]['status'])
    json_body = json.loads(resp[1].decode('UTF-8'))
    return {'status_code': status_code, 'json': json_body}


def request(url: str, method: str ='GET', data: dict =None):
    if method == 'GET':
        resp = requests.get(url)
    else:
        resp = requests.post(url, data)
    status_code = resp.status_code
    try:
        json_body = resp.json()
    except JSONDecodeError:
        raise InvalidUsage(code=404, description='The requested page could not be found')
    return {'status_code': status_code, 'json': json_body}
