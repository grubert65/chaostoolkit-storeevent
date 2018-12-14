# Chaostoolkit traceevent Control

This control allows you to store events on a configurable data store.
The data store can then be used to monitor events on a monitoring dashboard 
(such as Grafana) or to collect events on monitoring systems like Prometheus.

This control has to be added to each action you would like to monitor, adding 
this attribute:


```viml
    "configuration": {
        "
    },
    "method": [{
            "type": "action",
            ...
            "controls": [
                {
                    "name": "tracing",
                    "provider": {
                        "type": "python",
                        "module": "chaosdb.litedb"
                    }
                }
            ],
            "configuration": {
            }
        },
        {...}
    ]
```

A “scope” provider attribute can be set to “before”/“after” to get the control 
activated only before/after action execution (if missing the control is activate both before/after). 
