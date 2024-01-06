import uuid

import pytest
from django.test import TestCase
from fastapi.testclient import TestClient
from users.models import User

from real_state.asgi import app


@pytest.mark.django_db
class BaseTestCase(TestCase):
    def setUp(self):
        # Setting up the test client, user and cookies for the test.
        self.client = TestClient(app)
        self.password = "supersecret!"
        self.email = "a@a.com"
        self.user = User.objects.create(
            id=uuid.uuid4(),
            email=self.email,
            password=self.password,
        )
        self.cookies = {"user_id": str(self.user.id)}
        self.client.cookies = self.cookies
        self.base_django_url = str(self.client._base_url) + "/web/users/"
