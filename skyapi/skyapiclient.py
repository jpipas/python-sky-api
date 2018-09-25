# coding=utf-8
"""
Blackbaud SKY Api SDK
Documentation: https://developer.sky.blackbaud.com/docs/services/
"""
from __future__ import unicode_literals
import functools
import re


import requests
from requests.auth import HTTPBasicAuth
# Handle library reorganisation Python 2 > Python 3.
try:
    from urllib.parse import urljoin
    from urllib.parse import urlencode
except ImportError:
    from urlparse import urljoin
    from urllib import urlencode

import logging

_logger = logging.getLogger('skyapi.client')

SKY_API_ENDPOINT = 'https://api.sky.blackbaud.com/'sky-a

def _enabled_or_noop(fn):
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        if self.enabled:
            return fn(self, *args, **kwargs)
    return wrapper


class SkyAPIError(Exception):
    pass

class SkyAPITokenError(Exception):
    pass


class SkyAPIClient(object):
    """
    Sky API class to communicate with the Blackbaud API
    """
    def __init__(self, subscription_key=None, access_token=None, enabled=True, timeout=None, request_hooks=None, request_headers=None):

        super(SkyAPIClient, self).__init__()
        self.enabled = enabled
        self.timeout = timeout
        if access_token:
            self.auth = SkyAPIOAuth(access_token, subscription_key)
            self.base_url = SKY_API_ENDPOINT
        else:
            raise Exception("You must provide an OAuth access token")

        self.request_headers = request_headers or requests.utils.default_headers()
        self.request_hooks = request_hooks or requests.hooks.default_hooks()

    def _make_request(self, **kwargs):
        _logger.info(u'{method} Request: {url}'.format(**kwargs))
        if kwargs.get('json'):
            _logger.debug('PAYLOAD: {json}'.format(**kwargs))

        response = requests.request(**kwargs)

        _logger.debug(u'{method} Response: {status} {text}' \
                     .format(method=kwargs['method'], status=response.status_code, text=response.text))

        return response

    @_enabled_or_noop
    def _post(self, url, data=None):
        """
        Handle authenticated POST requests
        :param url: The url for the endpoint including path parameters
        :type url: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:data:`none` or :py:class:`dict`
        :returns: The JSON output from the API or an error message
        """
        url = urljoin(self.base_url, url)
        try:
            r = self._make_request(**dict(
                method='POST',
                url=url,
                json=data,
                auth=self.auth,
                timeout=self.timeout,
                hooks=self.request_hooks,
                headers=self.request_headers
            ))
        except requests.exceptions.RequestException as e:
            raise e
        else:
            if r.status_code == 401:
                raise SkyAPITokenError(r.json())
            if r.status_code == 400:
                # in case of a 500 error, the response might not be a JSON
                try:
                    error_data = r.json()
                except ValueError:
                    error_data = {"response": r}
                raise SkyAPIError(error_data)
            if r.status_code >= 403:
                # in case of a 500 error, the response might not be a JSON
                try:
                    error_data = r.json()
                except ValueError:
                    error_data = {"response": r}
            if r.status_code == 204:
                return None
            return r.json()

    @_enabled_or_noop
    def _get(self, url, **queryparams):
        """
        Handle authenticated GET requests
        :param url: The url for the endpoint including path parameters
        :type url: :py:class:`str`
        :param queryparams: The query string parameters
        :returns: The JSON output from the API
        """
        url = urljoin(self.base_url, url)
        if len(queryparams):
            url += '?' + urlencode(queryparams)
        try:
            r = self._make_request(**dict(
                method='GET',
                url=url,
                auth=self.auth,
                timeout=self.timeout,
                hooks=self.request_hooks,
                headers=self.request_headers
            ))
        except requests.exceptions.RequestException as e:
            raise e
        else:
            if r.status_code >= 400:
                raise SkyAPIError(r.json())
            return r.json()

    @_enabled_or_noop
    def _delete(self, url):
        """
        Handle authenticated DELETE requests
        :param url: The url for the endpoint including path parameters
        :type url: :py:class:`str`
        :returns: The JSON output from the API
        """
        url = urljoin(self.base_url, url)
        try:
            r = self._make_request(**dict(
                method='DELETE',
                url=url,
                auth=self.auth,
                timeout=self.timeout,
                hooks=self.request_hooks,
                headers=self.request_headers
            ))
        except requests.exceptions.RequestException as e:
            raise e
        else:
            if r.status_code >= 400:
                raise SkyAPIError(r.json())
            if r.status_code == 204:
                return
            return r.json()

    @_enabled_or_noop
    def _patch(self, url, data=None):
        """
        Handle authenticated PATCH requests
        :param url: The url for the endpoint including path parameters
        :type url: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:data:`none` or :py:class:`dict`
        :returns: The JSON output from the API
        """
        url = urljoin(self.base_url, url)
        try:
            r = self._make_request(**dict(
                method='PATCH',
                url=url,
                json=data,
                auth=self.auth,
                timeout=self.timeout,
                hooks=self.request_hooks,
                headers=self.request_headers
            ))
        except requests.exceptions.RequestException as e:
            raise e
        else:
            if r.status_code >= 400:
                raise SkyAPIError(r.json())
            return r.json()

    @_enabled_or_noop
    def _put(self, url, data=None):
        """
        Handle authenticated PUT requests
        :param url: The url for the endpoint including path parameters
        :type url: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:data:`none` or :py:class:`dict`
        :returns: The JSON output from the API
        """
        url = urljoin(self.base_url, url)
        try:
            r = self._make_request(**dict(
                method='PUT',
                url=url,
                json=data,
                auth=self.auth,
                timeout=self.timeout,
                hooks=self.request_hooks,
                headers=self.request_headers
            ))
        except requests.exceptions.RequestException as e:
            raise e
        else:
            if r.status_code >= 400:
                raise SkyAPIError(r.json())
            return r.json()


class SkyAPIOAuth(requests.auth.AuthBase):
    """
    Authentication class for authentication with OAuth2. Acquiring an OAuth2
    for Sky API can be done by following the instructions in the
    documentation found at
    https://developer.blackbaud.com/skyapi/docs/authorization/auth-code-flow
    """
    def __init__(self, access_token, subscription_key):
        """
        Initialize the OAuth and save the access token
        :param access_token: The access token provided by OAuth authentication
        :type access_token: :py:class:`str`
        :param subscription_key: The Blackbaud API Subscription key for your application
        :type subscription_key: :py:class:`str`
        """
        self._access_token = access_token
        self._subscription_key = subscription_key


    def __call__(self, r):
        """
        Authorize with the access token provided in __init__
        """
        r.headers['Authorization'] = 'Bearer ' + self._access_token
        r.headers['Bb-Api-Subscription-Key'] = self._subscription_key
        r.headers['Content-Type'] = 'application/json'
        return r

