# -*- coding: utf-8 -*-
import requests
from logzero import logger
from chaoslib.types import Configuration, Secrets
from .utils import can_connect_to

__all__ = [
    "running",
    "cleanup_control",
    "configure_control",
    "before_activity_control",
    "after_activity_control",
    "encode_payload_in_line_protocol",
]

# global defaults
influx_host = "localhost"
influx_port = 8086
influx_http_endpoint = "/write"
influx_database = "gatlingdb"


def running():
    """Test if the InfluxDB server is running"""

    return can_connect_to(influx_host, influx_port)


def cleanup_control():
    return 1


def configure_control(configuration: Configuration, secrets: Secrets):
    global influx_host
    global influx_port
    global influx_http_endpoint
    global influx_database

    influx = configuration.get(
        "influxdb",
        {
            "host": "localhost",
            "port": 8086,
            "http_endpoint": "/write",
            "database": "gatlingdb",
        },
    )

    influx_host = influx["host"]
    influx_port = influx["port"]
    influx_http_endpoint = influx["http_endpoint"]
    influx_database = influx["database"]

    return 1


def after_activity_control(context: dict, arguments=None):
    if context["type"] == "probe":
        return 1

    provider = context["provider"]

    return store_action("after", provider)


def before_activity_control(context: dict, arguments=None):
    if context["type"] == "probe":
        return 1

    provider = context["provider"]

    return store_action("before", provider)


def store_action(scope, provider):

    # implement InfluxDB line protocol
    # using the requests lib
    # scope is a tag

    logger.debug("store_action")
    logger.debug("Scope: {}".format(scope))
    logger.debug("Influx host: {}".format(influx_host))
    logger.debug("Influx port: {}".format(influx_port))
    logger.debug("Influx endpoint: {}".format(influx_http_endpoint))
    logger.debug("Influx database: {}".format(influx_database))

    payload = ""

    # TODO the measurement should contains the experiment name label
    if provider["type"] == "python":
        payload = encode_payload_in_line_protocol(
            "chaos_toolkit.actions",
            tags={"experiment": "exp1", "scope": scope},
            fields=provider,
        )

    r = requests.post(
        "http://{}:{}{}".format(influx_host, influx_port, influx_http_endpoint),
        params={"db": influx_database},
        data=payload,
    )

    if r.status_code != 204:
        logger.error("Error sending data to InfluxDB: {}".format(r.json()))

    logger.debug("store_action ended")
    return 1


# Encodes payload
# Influx will automatically add the timestamp...
def encode_payload_in_line_protocol(measurement, fields: dict, tags={}):

    payload = measurement

    # never use quotes for tags...
    for k in sorted(tags):
        payload = "{},{}={}".format(payload, k, tags[k])

    payload = payload + " "

    #     import pdb; pdb.set_trace()
    for k, v in fields.items():
        if isinstance(v, str):
            payload = '{}{}="{}",'.format(payload, k, v)
        elif isinstance(v, dict):
            # TODO : we have to encode dicts properly...
            continue
        else:
            payload = "{}{}={},".format(payload, k, v)

    payload = payload.rstrip(",")
    return payload
