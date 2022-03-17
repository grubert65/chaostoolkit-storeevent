# -*- coding: utf-8 -*-
# a chaosdb control class to write events directly into grafana data store as
# annotations using the annotations HTTP API
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
    "post_event"
]

# global defaults
grafana_host = 'localhost'
grafana_port = 3000
grafana_annotation_api_endpoint = '/api/annotations'
grafana_user = None
grafana_pass = None
exp_start_time = int(round(time.time() * 1000))
exp_end_time = int(round(time.time() * 1000))


def cleanup_control():
    return 1


def configure_control(configuration: Configuration, secrets: Secrets):
    global grafana_host
    global grafana_port
    global grafana_annotation_api_endpoint
    global grafana_user
    global grafana_pass

    global exp_start_time
    global exp_end_time
    global dashboardId
    global only_actions
    global tags

    # defaults
    grafana = configuration.get('grafana', {})

    grafana_user = grafana.get('username')
    grafana_pass = grafana.get('password')
    grafana_host = grafana.get('host', 'localhost')
    grafana_port = grafana.get('port', 3000)
    exp_start_time = int(round(time.time() * 1000))
    exp_end_time = int(round(time.time() * 1000))
    dashboardId = grafana.get('dashboardId', 1)
    only_actions = grafana.get('only_actions', 0)
    tags = grafana.get('tags', [])
    grafana_annotation_api_endpoint = '/api/annotations'

    return 1


def running():
    """ Test if the Grafana server is running """

    return can_connect_to(grafana_host, grafana_port)


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

    my_tags = []
    my_tags.extend(tags)
    my_tags.extend(['chaostoolkit', 'experiment'])
    text = context['title']

    payload = {
        "dashboardId": dashboardId,
        "time": exp_start_time,
        "isRegion": True,
        "timeEnd": exp_end_time,
        "tags": my_tags,
        "text": text
    }

    return post_event(payload)


def before_method_control(context: dict, arguments=None):

    my_tags = []
    my_tags.extend(tags)
    my_tags.extend(['chaostoolkit', 'method',
                    'before', context['description']])
    text = context['title']

    payload = {
        "dashboardId": dashboardId,
        "tags": my_tags,
        "text": text
    }

    return post_event(payload)


def after_method_control(context: dict, arguments=None):

    my_tags = []
    my_tags.extend(tags)
    my_tags.extend(['chaostoolkit', 'method', 'after', context['description']])
    text = context['title']

    payload = {
        "dashboardId": dashboardId,
        "tags": my_tags,
        "text": text
    }

    return post_event(payload)


def before_activity_control(context: dict, arguments=None):

    if ((context['type'] != 'action') and (only_actions == 1)):
        return 1

    my_tags = []
    my_tags.extend(tags)
    my_tags.extend([
        'chaostoolkit',
        'activity',
        'before',
        context['type'],
        context['name']
    ])

    if (context['provider']['type'] == 'python'):
        my_tags.append(context['provider']['func'])

    text = f"[{context['type']}]:{context['name']}"

    payload = {
        "dashboardId": dashboardId,
        "tags": my_tags,
        "text": text
    }

    return post_event(payload)


def after_activity_control(context: dict, arguments=None):

    if ((context['type'] != 'action') and only_actions == 1):
        return 1

    my_tags = []
    my_tags.extend(tags)
    my_tags.extend([
        'chaostoolkit',
        'activity',
        'after',
        context['type'],
        context['name']
    ])

    if (context['provider']['type'] == 'python'):
        my_tags.append(context['provider']['func'])

    text = f"[{context['type']}]:{context['name']}"

    payload = {
        "dashboardId": dashboardId,
        "tags": my_tags,
        "text": text
    }

    return post_event(payload)


def post_event(payload):

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    data = json.dumps(payload)
    logger.debug("Sending annotation to grafana server {}:{}"
                 .format(grafana_host, grafana_port))
    logger.debug("Data:\n{}".format(data))
    r = requests.post("http://{}:{}{}".format(
        grafana_host,
        grafana_port,
        grafana_annotation_api_endpoint),
        auth=HTTPBasicAuth(grafana_user, grafana_pass) if grafana_user else None,
        headers=headers,
        data=data,
        timeout=5)

    ret = r.status_code
    logger.debug("Status code: {}".format(ret))
    return ret
