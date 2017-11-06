import json

from urllib2 import urlopen, Request, HTTPError

TOKEN = '5f60b1f2d3bbd64536edb1a8d03ff0b8a536049a'


class ClientException(Exception):
    pass


class GithubApi(object):
    """This class implements the Github api v3 authentication & request."""

    def request(self, url):
        """Send an authenticated request to the Github API."""
        request = Request(url)
        request.add_header('Authorization',
                           'token %s' % TOKEN)
        try:
            response = urlopen(request)
        except HTTPError:
            raise ClientException
        raw_data = response.read().decode('utf-8')
        data = json.loads(raw_data)
        return data
