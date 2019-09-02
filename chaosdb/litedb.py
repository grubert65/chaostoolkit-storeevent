# -*- coding: utf-8 -*-
import sqlite3
import json
import time
from shutil import which
from logzero import logger
from chaoslib.types import Configuration, Secrets

__all__ = [
    "running",
    "cleanup_control",
    "configure_control",
    "before_activity_control",
    "after_activity_control"
]

litedb_filename = ""


def running():
    return which('sqlite3')


def cleanup_control():
    return 1


def configure_control(c: Configuration, s: Secrets):
    #     import pdb; pdb.set_trace()
    global litedb_filename
    litedb_filename = c["litedb_filename"]
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
        stmt = "INSERT INTO actions \
                (event_time, scope, type, module, func, args) "\
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
