from django.urls import path
from .views import DeviceLatestAPIView, DeviceRangeAPIView

urlpatterns = [
    path("devices/<str:device_id>/latest/", DeviceLatestAPIView.as_view(), name="device-latest"),
    path("devices/<str:device_id>/range/", DeviceRangeAPIView.as_view(), name="device-range"),
]