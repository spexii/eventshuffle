"""
eventshuffle URL Configuration
"""
# Third party imports
from rest_framework import routers

# Django library imports
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path

# Local application imports
from eventshuffle.event import views

router = routers.DefaultRouter()
router.register(r'events', views.EventViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('', lambda request: HttpResponse("Welcome to the amazing event shuffler!"))
]
