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
    return InfluxConfig(
        url=settings.INFLUXDB_URL,
        token=settings.INFLUXDB_TOKEN,
        org=settings.INFLUXDB_ORG,
        bucket=settings.INFLUXDB_BUCKET,
    )


def get_influx_client() -> InfluxDBClient:
    cfg = get_influx_config()
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