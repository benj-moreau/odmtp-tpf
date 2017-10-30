import json

from urllib2 import urlopen, Request, HTTPError


API_ENDPOINT = 'https://api.twitter.com'
API_VERSION = '1.1'
REQUEST_TOKEN_URL = '%s/oauth2/token' % API_ENDPOINT
REQUEST_RATE_LIMIT = '%s/%s/application/rate_limit_status.json' % \
                     (API_ENDPOINT, API_VERSION)
ENCODED_BEARER_TOKEN = 'a0xFdDZ0eDVFQ0FEUjczZjAwdFlidThMRTpjWHlVWEtrYTBubzBYMmtySzE2QTZPSGxjVEd0Nmw3ZERFd0RKbEFYeFp1UWRoQ1YzUg=='


class ClientException(Exception):
    pass


class TwitterApi(object):
    """This class implements the Twitter's Application-only authentication & request."""

    def __init__(self):
        self.access_token = ''

    def request(self, url):
        """Send an authenticated request to the Twitter API."""
        if not self.access_token:
            self.access_token = self._get_access_token()
        request = Request(url)
        request.add_header('Authorization', 'Bearer %s' % self.access_token)
        try:
            response = urlopen(request)
        except HTTPError:
            raise ClientException
        raw_data = response.read().decode('utf-8')
        data = json.loads(raw_data)
        return data

    def rate_limit_status(self, resource=''):
        """Return a dict of rate limits by resource."""
        response = self.request(REQUEST_RATE_LIMIT)
        if resource:
            resource_family = resource.split('/')[1]
            return response['resources'][resource_family][resource]
        return response

    def get_access_token(self):
        request = Request(REQUEST_TOKEN_URL)
        request.add_header('Content-Type',
                           'application/x-www-form-urlencoded;charset=UTF-8')
        request.add_header('Authorization',
                           'Basic %s' % ENCODED_BEARER_TOKEN.decode('utf-8'))

        request_data = 'grant_type=client_credentials'.encode('ascii')
        request.data = request_data

        response = urlopen(request)
        raw_data = response.read().decode('utf-8')
        data = json.loads(raw_data)
        return data['access_token']

    def set_access_token(self, access_token):
        self.access_token = access_token
