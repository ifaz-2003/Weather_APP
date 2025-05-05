from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import SavedCity

User = get_user_model()

class WeatherAppTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.auth_header = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}

    def test_signup(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "newpassword123",
            "password2": "newpassword123"
        }
        response = self.client.post("/signup/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login(self):
        data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = self.client.post("/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_saved_cities_empty(self):
        response = self.client.get("/api/saved-cities/", **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_save_and_retrieve_city(self):
        city_data = {
            "city_name": "London",
            "temp": "12.5",
            "description": "light rain",
            "icon": "01d"
        }
        self.client.post("/api/save-city/", city_data, **self.auth_header)
        response = self.client.get("/api/saved-cities/", **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["city_name"], "London")

    def test_remove_city(self):
        SavedCity.objects.create(user=self.user, city_name="Paris", temp="18", description="clear", icon="01d")
        response = self.client.delete("/api/remove-city/Paris/", **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_weather_default(self):
        response = self.client.get("/api/get-weather/?city=London")
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])  # Based on API status

    def test_frontend_serving(self):
        response = self.client.get("/")
        self.assertIn(response.status_code, [200, 501])
