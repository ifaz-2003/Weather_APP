from django.urls import path
from .views import get_weather, login_api, signup_api, get_saved_cities, save_city, remove_city
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('api/weather/', get_weather, name='get_weather'),
    path("api/signup/", signup_api, name="signup_api"),
    path("api/login/", login_api, name="login_api"),
    path("api/saved-cities/", get_saved_cities, name="get_saved_cities"),
    path("api/save-city/", save_city, name="save_city"),
    path("api/remove-city/<str:city_name>/", remove_city, name="remove_city"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]