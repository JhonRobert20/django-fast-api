from unittest import mock

import pytest
from estates.constants import fake_estate

from real_state.mongodb import mongodb
from real_state.tests.test_base import BaseTestCase


@pytest.mark.django_db
class EstateEndpointsTest(BaseTestCase):
    @mock.patch("real_state.auth.check_exists_user")
    def test_get_one_estate(self, mock_is_logged):
        # Mocking the authentication check and removing all estates from MongoDB.
        mock_is_logged.return_value = True
        mongodb.remove_entire_collection()

        # Adding a fake estate to MongoDB and getting its ID.
        estate = fake_estate
        mongodb.update_many_estates([estate])
        estate_id = estate["id"]

        # Getting the estate using the estate ID and checking the response.
        response = self.client.get(f"/api/estate/estates/{estate_id}")
        assert response.status_code == 200
        assert response.json() == estate

        # Deleting the estate and checking that it's no longer in the DB.
        mongodb.delete_one_estate(estate["id"])
        count_estates = len(list(mongodb.filter_estates({"_id": estate["id"]})))
        assert count_estates == 0

    @mock.patch("real_state.auth.check_exists_user")
    def test_create_one_estate(self, mock_is_logged):
        # Mocking the authentication check and removing all estates from MongoDB.
        mock_is_logged.return_value = True
        mongodb.remove_entire_collection()

        # Adding a fake estate to MongoDB and checking the response.
        estate = fake_estate
        response = self.client.post("/api/estate/estates/", json=estate)
        assert response.status_code == 200

        # Checking that the estate was added to MongoDB and deleting it.
        mongo_state = list(mongodb.filter_estates({"_id": estate["id"]}))
        assert mongo_state[0].get("id") == estate["id"]
        mongodb.delete_one_estate(estate["id"])
        count_estates = len(list(mongodb.filter_estates({"_id": estate["id"]})))
        assert count_estates == 0

    @mock.patch("real_state.auth.check_exists_user")
    def test_get_all_estates(self, mock_is_logged):
        # Mocking the authentication check and removing all estates from MongoDB.
        mock_is_logged.return_value = True
        mongodb.remove_entire_collection()

        # Adding a fake estate to MongoDB and checking the response.
        estate = fake_estate
        mongodb.update_many_estates([estate])
        response = self.client.get("/api/estate/estates/")
        assert response.status_code == 200

        # Checking the response data and deleting the estate.
        assert response.json().get("total_results") == 1
        assert not response.json().get("has_next")
        assert not response.json().get("has_prev")
        assert response.json().get("pages") == 1
        assert response.json().get("page") == 1
        mongodb.remove_entire_collection()
        count_estates = len(list(mongodb.filter_estates({})))
        assert count_estates == 0

    def test_check_no_permission(self):
        # Checking that the endpoints return 401 when the user is not logged in.
        estate = fake_estate
        assert self.client.get("/api/estate/estates/").status_code == 401
        assert self.client.post("/api/estate/estates/", json=estate).status_code == 401
        assert self.client.get(f"/api/estate/estates/{estate['id']}").status_code == 401

        assert self.client.get(f"/api/estate/estates/{estate['id']}").status_code == 401
