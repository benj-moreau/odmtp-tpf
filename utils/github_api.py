import json

from urllib2 import urlopen, Request, HTTPError


class ClientException(Exception):
    pass


class GithubApi(object):
    """This class implements the Github api v3 authentication & request."""

    def request(self, url):
        """Send an unauthenticated request to the Github API."""
        request = Request(url)
        try:
            response = urlopen(request)
        except HTTPError:
            raise ClientException
        raw_data = response.read().decode('utf-8')
        data = json.loads(raw_data)
        return data
