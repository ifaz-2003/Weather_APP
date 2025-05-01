"""
URL configuration for weather_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib import admin
from django.urls import path, include, re_path
from weather.views import FrontendAppView
from django.views.static import serve
import os
from django.conf import settings



urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # API routes
# ✅ NEW
    path('api/', include('weather.urls')),

    # Static files from Vue build
    re_path(r'^js/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'weather_app/frontend/js')}),
    re_path(r'^css/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'weather_app/frontend/css')}),
    re_path(r'^img/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'weather_app/frontend/img')}),
    re_path(r'^favicon.ico$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'weather_app/frontend'), 'path': 'favicon.ico'}),

    # Frontend app fallback (Vue SPA)
    re_path(r'^.*$', FrontendAppView.as_view()),
]