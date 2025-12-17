from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
import os
@api_view(["GET"])
def api_root(request, format=None):
    codespace_name = os.environ.get("CODESPACE_NAME")
    if codespace_name:
        base_url = f"https://{codespace_name}-8000.app.github.dev"
    else:
        base_url = "http://localhost:8000"
    return Response({
        "activities": base_url + reverse("activity-list"),
        "profiles": base_url + reverse("profile-list"),
        "teams": base_url + reverse("team-list"),
    })
"""octofit_tracker URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from tracker_core.views import ActivityViewSet, ProfileViewSet, TeamViewSet

router = routers.DefaultRouter()
router.register(r"activities", ActivityViewSet, basename="activity")
router.register(r"profiles", ProfileViewSet, basename="profile")
router.register(r"teams", TeamViewSet, basename="team")

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('dj_rest_auth.urls')),
]
