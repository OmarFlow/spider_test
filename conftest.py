import pytest

from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    user = User.objects.create_user(username='test', password='testopass')
    client = APIClient()
    client.force_authenticate(user)
    return client
