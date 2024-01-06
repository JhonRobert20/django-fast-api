import pytest
from django.core.management import call_command
from django.test import TestCase
from users.models import User

from real_state.mongodb import mongodb


@pytest.mark.django_db
class EstateBaseTest(TestCase):
    def test_populate_command(self):
        call_command("populate")
        assert User.objects.count() == 10
        assert len(list(mongodb.filter_estates({}))) == 10
        mongodb.remove_entire_collection()
