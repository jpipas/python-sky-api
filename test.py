import unittest
from skyapi import SkyApi


SUBSCRIPTION_KEY=""
ACCESS_TOKEN = ""

class SkyApiTestCase(unittest.TestCase):
    def setUp(self):
        self.client = SkyApi(subscription_key=SUBSCRIPTION_KEY,access_token=ACCESS_TOKEN)

class TestSkyAPIMethods(SkyApiTestCase):

    def test_get_constituent(self):
       self.assertEqual(self.client.constituent.get(7)['last'], 'Pipas')


if __name__ == '__main__':
    unittest.main()