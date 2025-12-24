from django.conf import settings


def _flux_time_expr(t: str | None) -> str | None:
  if not t:
    return None
  t = t.strip()
  if t.startswith("-") or t.startswith("now("):
    return t
  return f'time(v: "{t}")'


def flux_device_range(device_id: str, start: str, stop: str | None, every: str | None):
    """
    start/stop are RFC3339 like:
      2025-12-23T00:00:00Z
    or start can be relative like:
      -1h, -7d
    every is optional window: e.g. "1m", "10m", "1h"
    """
    conf = getattr(settings, "INFLUXDB", {}) or {}
    bucket = conf.get("BUCKET") or getattr(settings, "INFLUXDB_BUCKET", None)
    meas = getattr(settings, "INFLUX_MEASUREMENT_METRICS", "metrics")

    start_expr = _flux_time_expr(start) or start
    stop_expr = _flux_time_expr(stop)
    stop_line = f', stop: {stop_expr}' if stop_expr else ""
    window = f'|> aggregateWindow(every: {every}, fn: mean, createEmpty: false)\n' if every else ""

    return f'''
from(bucket: "{bucket}")
  |> range(start: {start_expr}{stop_line})
  |> filter(fn: (r) => r._measurement == "{meas}")
  |> filter(fn: (r) => r.device_id == "{device_id}")
  |> filter(fn: (r) =>
      r._field == "temperature" or
      r._field == "pressure" or
      r._field == "humidity" or
      r._field == "light_intensity" or
      r._field == "tilt" or
      r._field == "ToF" or
      r._field == "noise" or
      r._field == "forecast_temperature" or
      r._field == "forecast_pressure" or
      r._field == "forecast_humidity"
  )
  {window}
  |> pivot(rowKey:["time_stamp"], columnKey: ["_field"], valueColumn: "_value")
  |> keep(columns: ["time_stamp","device_id","temperature","pressure","humidity","light_intensity","tilt","ToF","forecast_temperature","forecast_pressure","forecast_humidity"])
  |> sort(columns: ["time_stamp"], desc: false)
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
        r._field == "noise" or
        r._field == "ToF" or
        r._field == "forecast_temperature" or
        r._field == "forecast_pressure" or
        r._field == "forecast_humidity"
    )
    |> last()

data
  |> pivot(rowKey:["time_stamp"], columnKey: ["_field"], valueColumn: "_value")
  |> keep(columns: ["time_stamp","device_id","temperature","pressure","humidity","light_intensity","tilt","ToF","forecast_temperature","forecast_pressure","forecast_humidity"])
  |> sort(columns: ["time_stamp"], desc: true)
  |> limit(n: 1)
'''
