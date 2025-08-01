"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.templatetags.static import static
from django.urls import path, include
from .views import get_pricing, get_websocket_pricing, index

app_name = "pricing"

handler404 = 'views.handler404'

urlpatterns = [
    path('', index),
    path('<str:exchange>/<str:symbol_a>/<str:symbol_b>/', get_pricing),
    # websocket
    path('pricing/', get_websocket_pricing),
]
