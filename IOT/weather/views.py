from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .Serializers import DeviceReadingSerializer
from .Influx import query_flux
from .queries import flux_device_range, flux_device_latest


def normalize_row(row: dict) -> dict:
    """
    Convert Influx row dict into API-friendly shape.
    In pivoted rows, time is in "_time".
    """
    return {
        "time_stamp": row.get("time_stamp"),
        "device_id": row.get("device_id"),
        "temperature": row.get("temperature"),
        "pressure": row.get("pressure"),
        "humidity": row.get("humidity"),
        "light_intensity": row.get("light_intensity"),
        "tilt": row.get("tilt"),
        "ToF": row.get("ToF"),
        "noise": row.get("noise"),
        "forecast_temperature": row.get("forecast_temperature"),
        "forecast_pressure": row.get("forecast_pressure"),
        "forecast_humidity": row.get("forecast_humidity"),
    }


class DeviceLatestAPIView(APIView):
    """
    GET /api/devices/{device_id}/latest/
    """

    def get(self, device_id: str):
        flux = flux_device_latest(device_id=device_id)
        rows = query_flux(flux)
        if not rows:
            return Response({"detail": "No data"}, status=status.HTTP_404_NOT_FOUND)

        payload = normalize_row(rows[0])
        ser = DeviceReadingSerializer(data=payload)
        ser.is_valid(raise_exception=True)
        return Response(ser.data)


class DeviceRangeAPIView(APIView):
    """
    GET /api/devices/{device_id}/range/?start=-1h&stop=...&every=10m
    Examples:
      start=-1h
      start=-7d
      start=2025-12-20T00:00:00Z
    stop is optional, every is optional
    """

    def get(self, request, device_id: str):
        start = request.query_params.get("start", "-1h")
        stop = request.query_params.get("stop")  # optional RFC3339
        every = request.query_params.get("every")  # optional like 1m/10m/1h

        flux = flux_device_range(device_id=device_id, start=start, stop=stop, every=every)
        rows = query_flux(flux)

        payload = [normalize_row(r) for r in rows]
        ser = DeviceReadingSerializer(data=payload, many=True)
        ser.is_valid(raise_exception=True)
        return Response(ser.data)
