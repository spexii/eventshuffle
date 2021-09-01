# Standard library imports
import os
import unittest

# Third party imports
from rest_framework.test import APIClient


class TestAPIAccess(unittest.TestCase):
    def setUp(self):
        # Initialize the client for making request and the API url to use
        self.client = APIClient()
        self.api_root = "/api/v1/"

    def test_0001_api_version_redirect(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, self.api_root)

    def test_0002_list_events(self):
        # This is just testing if the listing endpoint works
        response = self.client.get(f"{self.api_root}events/")
        self.assertEqual(response.status_code, 200)
