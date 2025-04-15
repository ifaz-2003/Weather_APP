
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

from django.test import SimpleTestCase
from django.urls import reverse

class URLTests(SimpleTestCase):

    def login_url(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def weather_url(self):
        response = self.client.get('/weather/')
        self.assertEqual(response.status_code, 200)

    def hobbies_url(self):
        response = self.client.get('/hobbies/')
        self.assertEqual(response.status_code, 200)

    def savedCities_url(self):
        response = self.client.get('/preferences/')
        self.assertEqual(response.status_code, 200)


class GeolocationAndCityWeatherFetchTest(APITestCase):
    def setUp(self):
        # Create and authenticate a test user
        self.user = User.objects.create_user(username='geoUser', password='testpass123')
        token_response = self.client.post('/api/token/', {
            'username': 'geoUser',
            'password': 'testpass123'
        }).data
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_response['access'])

    def test_geolocation_weather_fetch(self):
        # coordinates for London 
        response = self.client.get('/api/weather/?lat=51.5074&lon=-0.1278')
        
        # Validate the response
        self.assertEqual(response.status_code, 200)
        self.assertIn('temp', response.json())
        self.assertIn('description', response.json())

    def test_valid_city_weather_search(self):
        # Test with a real city name
        response = self.client.get('/api/weather/?city=London')
        self.assertEqual(response.status_code, 200)
        self.assertIn('weather', response.json())

    def test_invalid_city_weather_search(self):
        # Test with a fake/invalid city name
        response = self.client.get('/api/weather/?city=NotARealCity123')
        self.assertIn(response.status_code, [400, 404])
        self.assertIn('error', response.json())



class SavedCitiesTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='citySaver', password='testpass123') #same as other classes , user login 
        token_response = self.client.post('/api/token/', {
            'username': 'citySaver',
            'password': 'testpass123'
        }).data
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_response['access'])

    def test_save_city(self):
        # Simulate saving a city
        data = {
            "city_name": "London",
            "temp": "15.2",
            "description": "Partly cloudy",
            "icon": "https://openweathermap.org/img/wn/03d@2x.png"
        }

        response = self.client.post('/api/save-city/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "City saved successfully")

    def test_get_saved_cities(self):
        # First save a city
        self.test_save_city()

        # Then retrieve saved cities
        response = self.client.get('/api/saved-cities/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['city_name'], "London")
