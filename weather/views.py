from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, get_user_model
from .models import CustomUser, SavedCity
from .forms import SignupForm
import requests
from django.http import JsonResponse
from django.conf import settings

# OpenWeather API Key (Use your own key)
API_KEY = "69ce9849eb65509427ae460da399e041"

def get_weather(request):
    city = request.GET.get("city", "London")  # Default to London
    if not city:
        return JsonResponse({"error": "City not provided"}, status=400)

    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

    try:
        weather_response = requests.get(weather_url)
        forecast_response = requests.get(forecast_url)

        if weather_response.status_code == 200 and forecast_response.status_code == 200:
            return JsonResponse({
                "weather": weather_response.json(),
                "forecast": forecast_response.json(),
            })
        else:
            return JsonResponse({"error": "Failed to fetch weather data"}, status=400)

    except requests.RequestException:
        return JsonResponse({"error": "Failed to connect to OpenWeather API"}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])  # Allows unauthenticated users to register
def signup_api(request):
    form = SignupForm(request.data)
    if form.is_valid():
        user = form.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": user.username,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        })
    return Response(form.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    username = request.data.get("username")
    password = request.data.get("password")

    # Support login via email or username
    User = get_user_model()
    if "@" in username:
        try:
            user_obj = User.objects.get(email=username)
            username = user_obj.username
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=400)

    user = authenticate(username=username, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": user.username,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        })
    return Response({"error": "Invalid credentials"}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_saved_cities(request):
    cities = SavedCity.objects.filter(user=request.user)
    city_data = [
        {
            "city_name": city.city_name,
            "temp": city.temp,
            "description": city.description,
            "icon": city.icon,
        }
        for city in cities
    ]
    return Response(city_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_city(request):
    city_name = request.data.get('city_name')
    temp = request.data.get('temp')
    description = request.data.get('description')
    icon = request.data.get('icon')

    if not city_name or not temp or not description or not icon:
        return Response({"error": "Missing weather data"}, status=400)

    # Check if the city is already saved for the user
    if SavedCity.objects.filter(user=request.user, city_name=city_name).exists():
        return Response({"error": "City is already saved"}, status=400)

    # Save the new city
    SavedCity.objects.create(
        user=request.user,
        city_name=city_name,
        temp=temp,
        description=description,
        icon=icon,
    )
    return Response({"message": "City saved successfully"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_city(request, city_name):
    SavedCity.objects.filter(user=request.user, city_name=city_name).delete()
    return Response({"message": "City removed successfully"})