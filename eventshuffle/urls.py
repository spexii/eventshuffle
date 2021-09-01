"""
eventshuffle URL Configuration
"""
# Third party imports
from rest_framework import routers

# Django library imports
from django.contrib import admin
from django.http import HttpResponse
from django.views.generic.base import RedirectView
from django.urls import include, path, re_path

# Local application imports
from eventshuffle.event import views

router = routers.DefaultRouter()
router.register(r'events', views.EventViewSet)

urlpatterns = [
    # API path including version number, resulting e.g. to /api/v1/events
    re_path(r'^api/(?P<version>(v1|v2))/', include(router.urls)),
    path('api/', RedirectView.as_view(url='/api/v1/', permanent=True), name='go-to-v1'),
    path('admin/', admin.site.urls),
    path('', lambda request: HttpResponse("Welcome to the amazing event shuffler!"))
]
