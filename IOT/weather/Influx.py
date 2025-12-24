from dataclasses import dataclass
from influxdb_client import InfluxDBClient
from django.conf import settings


@dataclass(frozen=True)
class InfluxConfig:
    url: str
    token: str
    org: str
    bucket: str


def get_influx_config() -> InfluxConfig:
    # Support either a dict-style `INFLUXDB` setting or legacy individual settings.
    conf = getattr(settings, "INFLUXDB", {}) or {}
    return InfluxConfig(
        url=conf.get("URL") or getattr(settings, "INFLUXDB_URL", None),
        token=conf.get("TOKEN") or getattr(settings, "INFLUXDB_TOKEN", None),
        org=conf.get("ORG") or getattr(settings, "INFLUXDB_ORG", None),
        bucket=conf.get("BUCKET") or getattr(settings, "INFLUXDB_BUCKET", None),
    )


def get_influx_client() -> InfluxDBClient:
    cfg = get_influx_config()
    missing = [k for k, v in (("url", cfg.url), ("token", cfg.token), ("org", cfg.org)) if not v]
    if missing:
        raise RuntimeError(f"Missing InfluxDB configuration keys: {', '.join(missing)}")
    return InfluxDBClient(url=cfg.url, token=cfg.token, org=cfg.org)


def query_flux(flux: str):
    """
    Returns list[dict] where each dict is a row of values.
    We usually pivot in Flux so each row has columns for each field.
    """
    client = get_influx_client()
    try:
        tables = client.query_api().query(flux)
        rows = []
        for table in tables:
            for record in table.records:
                # record.values is a dict of columns -> values
                rows.append(record.values)
        return rows
    finally:
        client.close()