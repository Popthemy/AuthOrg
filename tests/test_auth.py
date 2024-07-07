import pytest
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from model_bakery import baker

from datetime import datetime, timedelta,timezone
from django.contrib.auth.hashers import make_password

User = settings.AUTH_USER_MODEL

@pytest.mark.django_db
class TestAuthenticationWithJwt:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.user = baker.make(User, 
                               email='user@example.com', 
                               first_name='John', 
                               last_name='Doe', 
                               password=make_password('testpassword'))
        

    def test_token_generation(self):
        token = RefreshToken.for_user(self.user)
        decoded_token = token.access_token.payload

        assert decoded_token['user_id'] == str(self.user.id)
        assert 'exp' in decoded_token

        # Calculate the token expiration time
        token_expiry = datetime.now(timezone.utc) + timedelta(seconds=decoded_token['exp'] - int(datetime.now(timezone.utc).timestamp()))

        # Subtract one second as a buffer
        token_expiry = token_expiry + timedelta(seconds=-1)

        assert datetime.now(timezone.utc) < token_expiry < datetime.now(timezone.utc) + timedelta(days=5)

    def test_login_returns_200(self, api_client):
        response = api_client.post('/auth/login/', {'email': self.user.email, 'password': 'testpassword'})
        assert response.status_code == status.HTTP_200_OK
        assert 'accessToken' in response.data['data']
        assert response.data['data']['user']['email'] == self.user.email

    def test_login_failure_returns_401(self, api_client):
        response = api_client.post('/auth/login/', {'email': self.user.email, 'password': 'wrongpassword'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'accessToken' not in response.data.get('data', {})
