# -*- coding: utf-8 -*-
# NOTE: under rewrite...
import sqlite3
import json
import time
import requests
from logzero import logger
from chaoslib.types import Configuration, Secrets

__all__ = [
    "cleanup_control",
    "configure_control",
    "before_activity_control",
    "after_activity_control"
]

# global defaults
influx_host         = "localhost"
influx_port         = 8086
influx_http_endpoint= "/write"
influx_database     = "gatlingdb"

def cleanup_control():
    return 1


def configure_control(c: Configuration, s: Secrets):
#     import pdb; pdb.set_trace()
    global influx_host
    global influx_port
    global influx_http_endpoint
    global influx_database
    influx_host          = c["influx_host"]
    influx_port          = c["influx_port"]
    influx_http_endpoint = c["influx_http_endpoint"]
    influx_database      = c["influx_database"]
    return 1


def after_activity_control(context: dict, arguments=None):
    if context['type'] == 'probe':
        return 1

    provider = context['provider']

    return store_action("after", provider)


def before_activity_control(context: dict, arguments=None):
    if context['type'] == 'probe':
        return 1

    provider = context['provider']

    return store_action("before", provider)


def store_action(scope, provider):

    # implement InfluxDB line protocol
    # using the requests lib
    # scope is a tag 

#     try:
    logger.debug("store_action")
    logger.debug("Scope: {}".format(scope))
#     import pdb; pdb.set_trace()
    global litedb_filename
    logger.debug("sqlite db file: {}".format(litedb_filename))
    conn = sqlite3.connect(litedb_filename)
#     conn = sqlite3.connect('./trace.db')
    c = conn.cursor()
    stmt = ""
    args = ""
    if 'arguments' in provider:
        args = json.dumps(json.dumps(provider['arguments']))

    if provider['type'] == 'python':
        stmt = "INSERT INTO actions (event_time, scope, type, module, func, args) "\
            "VALUES({},'{}','{}','{}','{}','{}')".format(
                time.time(),
                scope,
                provider['type'],
                provider['module'],
                provider['func'],
                args
            )

    if stmt != "":
        logger.debug("Going to execute cmd: {}".format(stmt))
        c.execute(stmt)
        conn.commit()

    conn.close()
    logger.debug("after_activity_control:end")
#     except:
#         logger.error("Error inserting action")

    return 1
