from django.urls import path
from .views import get_weather, login_api, signup_api, get_saved_cities, save_city, remove_city
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('api/weather/', get_weather, name='get_weather'),
    path("signup/", signup_api, name="signup_api"),
    path("login/", login_api, name="login_api"),
    path("saved-cities/", get_saved_cities, name="get_saved_cities"),
    path("save-city/", save_city, name="save_city"),
    path("remove-city/<str:city_name>/", remove_city, name="remove_city"),
]