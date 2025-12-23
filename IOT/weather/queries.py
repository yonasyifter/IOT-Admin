from django.conf import settings


def flux_device_range(device_id: str, start: str, stop: str | None, every: str | None):
    """
    start/stop are RFC3339 like:
      2025-12-23T00:00:00Z
    or start can be relative like:
      -1h, -7d
    every is optional window: e.g. "1m", "10m", "1h"
    """
    bucket = settings.INFLUXDB_BUCKET
    meas = settings.INFLUX_MEASUREMENT_METRICS

    stop_line = f', stop: time(v: "{stop}")' if stop else ""
    window = f'|> aggregateWindow(every: {every}, fn: mean, createEmpty: false)\n' if every else ""

    return f'''
from(bucket: "{bucket}")
  |> range(start: {start}{stop_line})
  |> filter(fn: (r) => r._measurement == "{meas}")
  |> filter(fn: (r) => r.device_id == "{device_id}")
  |> filter(fn: (r) =>
      r._field == "temperature" or
      r._field == "pressure" or
      r._field == "humidity" or
      r._field == "light_intensity" or
      r._field == "tilt" or
      r._field == "ToF" or
      r._field == "forecast_temperature" or
      r._field == "forecast_pressure" or
      r._field == "forecast_humidity"
  )
  {window}
  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
  |> keep(columns: ["_time","device_id","temperature","pressure","humidity","light_intensity","tilt","ToF","forecast_temperature","forecast_pressure","forecast_humidity"])
  |> sort(columns: ["_time"], desc: false)
'''


def flux_device_latest(device_id: str):
    bucket = settings.INFLUXDB_BUCKET
    meas = settings.INFLUX_MEASUREMENT_METRICS

    # get latest point per field, then pivot
    return f'''
data =
  from(bucket: "{bucket}")
    |> range(start: -30d)
    |> filter(fn: (r) => r._measurement == "{meas}")
    |> filter(fn: (r) => r.device_id == "{device_id}")
    |> filter(fn: (r) =>
        r._field == "temperature" or
        r._field == "pressure" or
        r._field == "humidity" or
        r._field == "light_intensity" or
        r._field == "tilt" or
        r._field == "ToF" or
        r._field == "forecast_temperature" or
        r._field == "forecast_pressure" or
        r._field == "forecast_humidity"
    )
    |> last()

data
  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
  |> keep(columns: ["_time","device_id","temperature","pressure","humidity","light_intensity","tilt","ToF","forecast_temperature","forecast_pressure","forecast_humidity"])
  |> sort(columns: ["_time"], desc: true)
  |> limit(n: 1)
'''