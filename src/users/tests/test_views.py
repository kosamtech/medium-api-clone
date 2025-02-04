import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from users.views import CustomerUserDetailsView


User = get_user_model()


@pytest.mark.django_db
def test_authentication_requirement(normal_user):
    client = APIClient()
    url = reverse("user-details")
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    client.force_authenticate(user=normal_user)
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_retrieve_user_detail(normal_user):
    client = APIClient()
    client.force_authenticate(user=normal_user)
    url = reverse("user-details")

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == normal_user.email
    assert response.data["first_name"] == normal_user.first_name
    assert response.data["last_name"] == normal_user.last_name


@pytest.mark.django_db
def test_get_query_empty(normal_user):
    client = APIClient()
    client.force_authenticate(user=normal_user)
    url = reverse("user-details")
    response = client.get(url)

    view = CustomerUserDetailsView()
    view.request = response.wsgi_request

    queryset = view.get_queryset()

    assert queryset.count() == 0
