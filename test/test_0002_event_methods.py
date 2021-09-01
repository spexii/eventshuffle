# Standard library imports
from datetime import date, timedelta
import os
import unittest

# Third party imports
from rest_framework.test import APIClient

# Local application imports
from eventshuffle.event.models import Event


class TestEventMethods(unittest.TestCase):
    # The id of the created event is stored here and used class-wide
    event_id = None

    def setUp(self):
        # Initialize the client for making request and the API url to use
        self.client = APIClient()
        self.api_root = "/api/v1/"

        # Three valid dates starting from today
        self.valid_dates = [date.today() + timedelta(days=x) for x in range(3)]

        # Create random names for two different voters
        self.voters = ["Aaa123", "Bbb456"]

    def test_0001_create_event_without_data(self):
        response = self.client.post(f"{self.api_root}events/")
        self.assertNotEqual(response.status_code, 201)

    def test_0002_create_event_with_invalid_data(self):
        # Event can't be created with date(s) in the past
        invalid_event_data = {
            "name": "Summer party",
            "dates": ["2021-08-28", "2021-08-29", "2021-08-30"]
        }

        response = self.client.post(f"{self.api_root}events/", invalid_event_data, format='json')
        self.assertNotEqual(response.status_code, 201)

    def test_0003_create_event(self):
        event_data = {
            "name": "Summer party",
            "dates": self.valid_dates
        }

        response = self.client.post(f"{self.api_root}events/", event_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.__class__.event_id = response.data["id"]

    def test_0004_check_created_event(self):
        response = self.client.get(f"{self.api_root}events/{self.__class__.event_id}/")
        self.assertEqual(response.status_code, 200)

        event_dates = [v["date"] for v in response.data["votes"]]
        self.assertEqual(set(self.valid_dates), set(event_dates))

    def test_0005_vote_invalid_dates(self):
        # Try to vote for dates that doesn't exist for this event
        invalid_vote_data = {
            "name": self.voters[0],
            "votes": [
                "2021-08-29",
                "2021-08-30"
            ]
        }

        response = self.client.post(
            f"{self.api_root}events/{self.__class__.event_id}/vote/",
            invalid_vote_data,
            format='json'
        )
        self.assertNotEqual(response.status_code, 200)
    
    def test_0006_vote_valid_dates(self):
        # Vote two dates with the first voter
        valid_vote_data = {
            "name": self.voters[0],
            "votes": [
                self.valid_dates[0],
                self.valid_dates[1]
            ]
        }

        response = self.client.post(
            f"{self.api_root}events/{self.__class__.event_id}/vote/",
            valid_vote_data,
            format='json'
        )
        self.assertEqual(response.status_code, 200)

        # Vote single date with the second voter
        valid_vote_data2 = {
            "name": self.voters[1],
            "votes": [
                self.valid_dates[0]
            ]
        }

        response = self.client.post(
            f"{self.api_root}events/{self.__class__.event_id}/vote/",
            valid_vote_data2,
            format='json'
        )
        self.assertEqual(response.status_code, 200)

    def test_0007_check_suitable_dates(self):
        # Get results for the voting. This endpoint returns only the
        # dates that are suitable for all participants.
        response = self.client.get(f"{self.api_root}events/{self.__class__.event_id}/results/")

        # Add the suitable dates to a list
        suitable_dates = [sd["date"] for sd in response.data["suitable_dates"]]

        # The only suitable date is the first valid date (at index 0), since
        # it has votes from both of the voters. The following check compares
        # that single date to the list of suitable dates from the response.
        # The suitable dates should be a list containing only one item, but
        # just in case lists are compared with set() that orderers the lists
        self.assertEqual(
            set([self.valid_dates[0]]),
            set(suitable_dates)
        )
        
    @classmethod
    def tearDownClass(self):
        # Delete the event created within tests
        Event.objects.filter(id=self.event_id).delete()
