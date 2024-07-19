import pytest
from model_bakery import baker
from rest_framework import status
from django.conf import settings
from django.urls import reverse_lazy
from api.models import Organisation

User = settings.AUTH_USER_MODEL


@pytest.mark.django_db
class TestRegisterEndpoint:

    def test_register_user_success_default_org_reuturns_201(self, api_client):
        # Test case: Ensure a user is registered successfully when no organisation details are provided.
        url = reverse_lazy('register_user')

        # Prepare registration data
        register_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'password': 'testpassword001'
        }

        # Make request to register endpoint
        response = api_client.post(url, register_data, format='json')

        user = response.data['data']['user']['user_id']
        organisation = Organisation.objects.get(user=user)

        # Assert the response
        assert response.status_code == status.HTTP_201_CREATED
        assert 'accessToken' in response.data['data']
        assert 'user' in response.data['data']
        assert response.data['data']['user']['email'] == 'johndoe@example.com'
        assert organisation

    def test_login_user_success_returns_200(self, api_client):
        # Test case: Ensure a user is logged in successfully when valid credentials are provided.

        # First, register a user
        url_register = reverse_lazy('register_user')

        # Replace 'login_user' with your actual login endpoint name
        url_login = reverse_lazy('login_user')

        # Prepare registration data
        register_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'password': 'testpassword001'
        }

        # Make request to register endpoint
        response = api_client.post(url_register, register_data, format='json')

        # Login with credentials
        login_data = {
            'email': 'johndoe@example.com',
            'password': 'testpassword001'
        }

        login_response = api_client.post(url_login, login_data, format='json')

        # Assert the login response
        assert login_response.status_code == status.HTTP_200_OK, f"Expected status code 200 but got {login_response.status_code}: {login_response.data}"
        assert 'accessToken' in login_response.data['data'], "Access token missing in login response"
        assert 'user' in login_response.data['data'], "User details missing in login response"
        assert login_response.data['data']['user']['email'] == login_data[
            'email'], f"Expected email {login_data['email']} but got {login_response.data['data']['user']['email']}"

    def test_missing_required_fields_returns_422(self, api_client):
        # Test case: Ensure registration fails if required fields (firstName, lastName, email, password) are missing.

        # Test each required field missing scenario
        missing_field_tests = [
            ({  # Missing firstName
                "last_name": "Doe",
                "email": "johndoe@example.com",
                "password": "testpassword",
                "phone": "1234567890"
            }, "first_name"),

            ({  # Missing lastName
                "first_name": "John",
                "email": "johndoe@example.com",
                "password": "testpassword",

            }, "last_name"),
            ({  # Missing email
                "first_name": "John",
                "last_name": "Doe",
                "password": "testpassword",

            }, "email"),
            ({  # Missing password
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@example.com",

            }, "password"),
        ]

        for data, missing_field in missing_field_tests:
            response = api_client.post(reverse_lazy(
                'register_user'), data, format='json')
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, f"Expected status code 422 but got {response.status_code}"
            assert missing_field in response.data[
                'errors'], f"Expected error for missing field {missing_field} but got {response.data['errors']}"
            assert len(response.data['errors'][missing_field]
                       ) == 1, f"Expected exactly one error message for field {missing_field} but got {len(response.data['errors'][missing_field])}"

    def test_duplicate_email_registration_returns_422(self, api_client):
        # Test case: Ensure registration fails if a duplicate email is used.

        # Register a user first
        register_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "password": "testpassword",
            "phone": "1234567890"
        }
        api_client.post(reverse_lazy('register_user'),
                        register_data, format='json')

        # Attempt to register with the same email
        duplicate_register_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "johndoe@example.com",  # Same email as above
            "password": "testpassword2",
            "phone": "9876543210"
        }
        response = api_client.post(reverse_lazy(
            'register_user'), duplicate_register_data, format='json')

        # Assert the response
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, f"Expected status code 422 but got {response.status_code}"
        assert 'email' in response.data[
            'errors'], f"Expected error for duplicate email but got {response.data['errors']}"
        assert len(response.data['errors']['email']
                   ) == 1, f"Expected exactly one error message for email field but got {len(response.data['errors']['email'])}"
