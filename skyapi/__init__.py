# coding=utf-8
"""
Sky API SDK
https://developer.sky.blackbaud.com/docs/services/
"""
# API Client
from skyapi.skyapiclient import SkyAPIClient

# Constituent
from skyapi.entities.constituent import Constituent


class SkyApi(SkyAPIClient):

    def __init__(self, *args, **kwargs):
        """
        Initialize the class with your access_key and subscription_key and attach all of your endpoints
        """
        super(SkyApi, self).__init__(*args, **kwargs)

        self.constituent = Constituent(self)
