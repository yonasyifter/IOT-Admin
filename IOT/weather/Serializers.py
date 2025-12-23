from rest_framework import serializers


class DeviceReadingSerializer(serializers.Serializer):
    # timestamp
    time = serializers.DateTimeField(required=True)

    # device identity
    device_id = serializers.CharField(required=True)

    # your fields
    temperature = serializers.FloatField(required=False, allow_null=True)
    pressure = serializers.FloatField(required=False, allow_null=True)
    humidity = serializers.FloatField(required=False, allow_null=True)
    light_intensity = serializers.FloatField(required=False, allow_null=True)
    tilt = serializers.FloatField(required=False, allow_null=True)
    ToF = serializers.FloatField(required=False, allow_null=True)

    # optional forecast fields (only if you store them)
    forecast_temperature = serializers.FloatField(required=False, allow_null=True)
    forecast_pressure = serializers.FloatField(required=False, allow_null=True)
    forecast_humidity = serializers.FloatField(required=False, allow_null=True)