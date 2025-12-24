from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(["GET"])
def api_root(request, format=None):
    return Response({
        "devices_latest": reverse("device-latest", args=["<device_id>"], request=request),
        "devices_range": reverse("device-range", args=["<device_id>"], request=request),
        "api_auth": "/api-auth/login/",
    })


urlpatterns = [
    path("admin/", admin.site.urls),
    path("weather/", include("weather.urls")),
    path("api/", api_root),
    path("api-auth/", include(("rest_framework.urls", "rest_framework"), namespace="rest_framework")),
]
    