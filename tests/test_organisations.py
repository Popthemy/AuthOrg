import pytest
from model_bakery import baker
from rest_framework import status
from django.conf import settings
from django.contrib.auth.hashers import make_password
from api.models import Organisation

User = settings.AUTH_USER_MODEL


@pytest.mark.django_db
class TestOrganisationAccess:

    def setup_method(self):
        self.user1 = baker.make(User,
                                email='demouser@example.com',
                                first_name='John',
                                last_name='Doe',
                                password=make_password('testpassword001'))

        self.user2 = baker.make(User,
                                email='testuser@example.com',
                                first_name='Joh',
                                last_name='Doe',
                                password=make_password('testpasswor002'))

        self.organisation1 = baker.make('Organisation', name="Org1")

        self.organisation2 = baker.make('Organisation', name="Org2")
        self.organisation1.user.add(self.user1)
        self.organisation2.user.add(self.user2)

        # Save organisations to ensure IDs are set
        self.organisation1.save()
        self.organisation2.save()


    def test_user_cannot_access_other_organisation_data_returns_403(self, api_client):
        # User1 logs in
        login_response = api_client.post(
            '/auth/login/', {'email': self.user1.email, 'password': 'testpassword001'})
        assert login_response.status_code == status.HTTP_200_OK, f"Login failed: {login_response.data}"

        # Extracting accessToken from the response data
        access_token = login_response.data.get('data', {}).get('accessToken')

        assert access_token, "Access token not found in login response"

        api_client.credentials(HTTP_AUTHORIZATION=f'JWT {access_token}')

        # User1 tries to access Organisation2's data
        response = api_client.get(
            f'/api/organisations/{self.organisation2.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN, f"Expected 403 Forbidden, but got {response.status_code}: {response.data}"

    def test_user_can_access_their_own_organisation_data_returns_200(self, api_client):
        # User1 logs in
        login_response = api_client.post(
            '/auth/login/', {'email': self.user1.email, 'password': 'testpassword001'})
        assert login_response.status_code == status.HTTP_200_OK, f"Login failed: {login_response.data}"

        # Extracting accessToken from the response data
        access_token = login_response.data.get('data', {}).get('accessToken')

        assert access_token, "Access token not found in login response"

        api_client.credentials(HTTP_AUTHORIZATION=f'JWT {access_token}')

        # User1 accesses their own Organisation1's data
        response = api_client.get(
            f'/api/organisations/{self.organisation1.id}/')
        assert response.status_code == status.HTTP_200_OK, f"Unexpected status code: {response.status_code}, Response data: {response.data}"
        assert response.data['data']['name'] == self.organisation1.name

    def test_user_cannot_see_other_organisation_users_returns_403(self, api_client):
        # User1 logs in
        login_response = api_client.post(
            '/auth/login/', {'email': self.user1.email, 'password': 'testpassword001'})
        assert login_response.status_code == status.HTTP_200_OK, f"Login failed: {login_response.data}"

        api_client.credentials(HTTP_AUTHORIZATION='JWT ' +
                               login_response.data['data']['accessToken'])

        # User1 tries to access users from Organisation2
        response = api_client.get(
            f'/api/organisations/{self.organisation2.id}/users/')
        assert response.status_code == status.HTTP_403_FORBIDDEN, f"Unexpected status code: {response.status_code}, Response data: {response.data}"

    def test_user_can_see_their_own_organisation_users_200(self, api_client):
        # User1 logs in
        login_response = api_client.post(
            '/auth/login/', {'email': self.user1.email, 'password': 'testpassword001'})
        assert login_response.status_code == status.HTTP_200_OK, f"Login failed: {login_response.data}"

        api_client.credentials(HTTP_AUTHORIZATION='JWT ' +
                               login_response.data['data']['accessToken'])

        # User1 accesses users from Organisation1
        response = api_client.get(
            f'/api/organisations/{self.organisation1.id}/users/')
        assert response.status_code == status.HTTP_200_OK, f"Unexpected status code: {response.status_code}, Response data: {response.data}"

        # Check if the response contains user1's email
        user_emails = [user['email']
                       for user in response.data['data']['users_in_organisation']]
        assert self.user1.email in user_emails, f"User's email {self.user1.email} not found in response"
