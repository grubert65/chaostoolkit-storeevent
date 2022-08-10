# -*- coding: utf-8 -*-
# a chaosdb control class to write events directly into grafana data store as
# annotations using the annotations API
# The configuration section for this control is keyed "grafana".
# grafana configuration section attributes:
#
# host              : the grafana server fqdn
# port              : the grafana service port
# protocol          : http/https (defaults to http if not set)
# api_token         : grafana API token
# cert_file         : file where the TSL certificate is stored
# username          : the simple auth user name
# password          : the simple auth password
# dashboardId       : a specific dashboard ID (all in case it's not specified)
# only_actions      : a boolean flag to send only actions or probes as well
#                     (defaults to false)
# tags              : a list of custom tags to tag annotations
# annotation_api_endpoint: defaults to '/api/annotations'
#
# Among the other parameters that can be added to the  paylod:
# The "time" (millisecs since epoch) attribute can be added to each payload
# to set the annotation time, if missing grafana will consider it's
# process time for the event.

import requests
import json
from requests.auth import HTTPBasicAuth
import time
import datetime
from logzero import logger
from chaoslib.types import Configuration, Secrets
from .utils import can_connect_to

__all__ = [
    "running",
    "cleanup_control",
    "configure_control",
    "before_experiment_control",
    "after_experiment_control",
    "before_method_control",
    "after_method_control",
    "before_activity_control",
    "after_activity_control",
    "post_event",
]


def cleanup_control():
    return 1


def configure_control(configuration: Configuration, secrets: Secrets):
    global grafana
    global exp_start_time
    global exp_end_time

    # defaults
    grafana = configuration.get("grafana")
    if grafana is None:
        raise Exception("grafana configuration section not found")
    exp_start_time = int(round(time.time() * 1000))
    exp_end_time = int(round(time.time() * 1000))

    for server in grafana:
        if "host" not in server:
            raise Exception("Grafana server host not configured")
        if "port" not in server:
            raise Exception("Grafana server port not configured")
        if "protocol" not in server:
            server["protocol"] = "http"
        #         if 'dashboardId' not in server:
        #             server['dashboardId'] = 1
        if "only_actions" not in server:
            server["only_actions"] = 0
        if "annotation_api_endpoint" not in server:
            server["annotation_api_endpoint"] = "/api/annotations"
        if "tags" not in server:
            server["tags"] = []

    return 1


def running():
    """Test if all Grafana servers are running"""

    for server in grafana:
        if can_connect_to(grafana["host"], grafana["port"]) is false:
            return false
    return true


# Note: annotation region around the experiment is sent
# at experiment end
def before_experiment_control(context: dict, arguments=None):
    d = datetime.datetime.now()
    mill = int(d.microsecond / 1000)
    global exp_start_time
    exp_start_time = int(round(time.time() * 1000)) + mill
    return 1


def after_experiment_control(context: dict, arguments=None):
    global exp_start_time
    global exp_end_time

    exp_end_time = int(round(time.time() * 1000))

    for server in grafana:
        my_tags = []
        my_tags.extend(server["tags"])
        my_tags.extend(["chaostoolkit", "experiment"])

        payload = {
            "time": exp_start_time,
            "isRegion": True,
            "timeEnd": exp_end_time,
            "tags": my_tags,
            "text": context["title"],
        }
        post_event(server, payload)
    return 1


def before_method_control(context: dict, arguments=None):

    for server in grafana:
        my_tags = []
        my_tags.extend(server["tags"])
        my_tags.extend(["chaostoolkit", "method", "before", context["description"]])
        payload = {"tags": my_tags, "text": context["title"]}
        post_event(server, payload)
    return 1


def after_method_control(context: dict, arguments=None):

    for server in grafana:
        my_tags = []
        my_tags.extend(server["tags"])
        my_tags.extend(["chaostoolkit", "method", "after", context["description"]])
        payload = {"tags": my_tags, "text": context["title"]}
        post_event(server, payload)
    return 1


def before_activity_control(context: dict, arguments=None):

    for server in grafana:
        if (context["type"] != "action") and (server["only_actions"] == 1):
            continue
        my_tags = []
        my_tags.extend(server["tags"])
        my_tags.extend(
            ["chaostoolkit", "activity", "before", context["type"], context["name"]]
        )

        if context["provider"]["type"] == "python":
            my_tags.append(context["provider"]["func"])

        payload = {
            "dashboardId": server.get("dashboardId"),
            "tags": my_tags,
            "text": f"[{context['type']}]:{context['name']}",
        }

        post_event(server, payload)
    return 1


def after_activity_control(context: dict, arguments=None):

    for server in grafana:
        if (context["type"] != "action") and server["only_actions"] == 1:
            continue
        my_tags = []
        my_tags.extend(server["tags"])
        my_tags.extend(
            ["chaostoolkit", "activity", "after", context["type"], context["name"]]
        )

        if context["provider"]["type"] == "python":
            my_tags.append(context["provider"]["func"])
        payload = {
            "dashboardId": server.get("dashboardId"),
            "tags": my_tags,
            "text": f"[{context['type']}]:{context['name']}",
        }
        post_event(server, payload)
    return 1


def post_event(server: dict, payload: dict):

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + server["api_token"]
        if "api_token" in server
        else None,
    }

    data = json.dumps(payload)
    logger.debug(
        f"Sending annotation to grafana server {server['host']}:{server['port']}"
    )
    logger.debug(f"Data:\n{data}")
    r = requests.post(
        f"{server['protocol']}://{server['host']}:{server['port']}{server['annotation_api_endpoint']}",
        auth=HTTPBasicAuth(server["username"], server["password"])
        if "username" in server
        else None,
        verify=cert_file if "cert_file" in server else False,
        headers=headers,
        data=data,
        timeout=5,
    )

    ret = r.status_code
    logger.debug(f"Status code: {ret}")
    return ret
