from unittest import mock

import pytest
from django.urls import reverse

from real_state.tests.test_base import BaseTestCase


@pytest.mark.django_db
class UsersViewsTest(BaseTestCase):
    @mock.patch("users.views.AuthenticationForm")
    @mock.patch("users.views.authenticate")
    @mock.patch("users.views.login")
    def test_view_login(self, mock_login, mock_auth, mock_form):
        # Configuring mocks for the authentication, login, and form
        mock_auth.return_value = self.user
        mock_login.return_value = None
        mock_form_instance = mock_form.return_value
        mock_form_instance.is_valid.return_value = True
        mock_form_instance.cleaned_data = {
            "username": self.email,
            "password": self.password,
        }

        # Asserting the HTTP response status code for the pages
        home_page = self.client.get("/web/users/")
        assert home_page.status_code == 200

        login_page = self.client.get("/web/users/login")
        csrf_token = self.client.cookies["csrftoken"]
        assert login_page.status_code == 200

        register_page = self.client.get("/web/users/register")
        assert register_page.status_code == 200

        # Simulating a login attempt and asserting the HTTP response status code and URL
        login_response = self.client.post(
            "web/users/login",
            data={
                "csrfmiddlewaretoken": csrf_token,
                "username": self.email,
                "password": self.password,
            },
            headers={"X-CSRFToken": csrf_token},
        )
        assert login_response.status_code == 200
        assert "http://testserver/web" + reverse("home") == str(login_response.url)

        # Asserting that the authentication, login, and form functions were correct
        assert mock_auth.called
        assert mock_login.called
        assert mock_form.called
        assert mock_form_instance.is_valid.called
        assert mock_form_instance.cleaned_data.get("username") == self.email
        assert mock_form_instance.cleaned_data.get("password") == self.password

    @mock.patch("users.views.NewUserForm")
    @mock.patch("users.views.login")
    def test_register_request(self, mock_login, mock_form):
        # Configuring mocks for the login and form
        mock_login.return_value = None
        mock_form.return_value.is_valid.return_value = True
        mock_form.return_value.save.return_value = self.user
        register_page = self.client.get("/web/users/register")
        csrf_token = self.client.cookies["csrftoken"]
        assert register_page.status_code == 200

        # Simulating a registration attempt and asserting the HTTP response status code
        response = self.client.post(
            "/web/users/register",
            data={
                "csrfmiddlewaretoken": csrf_token,
                "email": self.email,
                "password1": self.password,
                "password2": self.password,
            },
            headers={"X-CSRFToken": csrf_token},
        )
        assert str(response.url) == self.base_django_url
