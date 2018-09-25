# coding=utf-8
"""
The base API object that allows constructions of various endpoint paths
"""
from __future__ import unicode_literals
from itertools import chain

# from skyapi.helpers import merge_results


class BaseApi(object):
    """
    Simple class to buid path for entities
    """

    def __init__(self, sky_client):
        """
        Initialize the class with you user_id and secret_key
        :param sky_client: The skyapi client connection
        :type sky_client: :mod:`skyapi.skyapiclient.SkyApiClient`
        """
        super(BaseApi, self).__init__()
        self._sky_client = sky_client
        self.entity = ''
        self.endpoint = ''
        self.version = 'v1'

    def _build_path(self, *args):
        """
        Build path with endpoint and args
        :param args: Tokens in the endpoint URL
        :type args: :py:class:`unicode`
        """
        return '/'.join(chain((self.entity,self.version,self.endpoint), map(str, args)))