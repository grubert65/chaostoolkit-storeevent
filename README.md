# Chaostoolkit storeevent Control

This control allows you to store events on a configurable data store.
The data store can then be used to monitor events on a monitoring dashboard 
or to collect events on monitoring systems like Prometheus.
The control currently implements the following drivers:

* an influx driver to store events on a InfluxDB time series database
* a grafana driver to store events on a Grafana server as annotations

The grafana driver supports the following authentication types:
- basic auth (username/password)
- bearer API token

To understand what a chaos-toolkit control is please refer to the official 
documentation on [controls](https://docs.chaostoolkit.org/reference/api/experiment/#controls).

## The Influx driver

InfluxDB is one of the most used time series data stores, it's implemented in
golang and therefore is pretty fast and very easy to install and set up.
Moreover, if you use Gatling for your performance input load simulations, it is
pretty simple to store Gatling metrics on InfluxDB as well (as the Influx server can be
configured to accept data in the graphite protocol), so you can use the 
same Influx data store for Gatling metrics and chaos toolkit events.

You can configure the Influx driver setting these parameters in the
configuration section (the values provided represent the defaults):

```
    "configuration": {
      "influxdb": {
        "host": "localhost",
        "port": 8086,
        "http_endpoint": "/write",
        "database": "gatlingdb"
      }
    }
```

Then, at the proper level, configure the control driver:

```
            "controls": [
                {
                    "name": "tracing",
                    "provider": {
                        "type": "python",
                        "module": "chaosdb.influx"
                    }
                }
            ],
```

## The Grafana driver

The Grafana driver can be quite convenient if you use grafana for your 
dashboards. The driver sends chaos-toolkit events directly to Grafana using
the Annotation HTTP API.
Moreover it is able to draw a region annotation around the whole experiment,
making experiment visualization more visible.


The grafana configuration section is keyed `"grafana"`.
The grafana driver accepts a list of configuration sections, one for each
grafana server you want to send annotations to.
Each section accepts the following configuration attributes:

|Attribute|Description|
|---------|-----------|
|host              | the grafana server fqdn|
|port              | the grafana service port|
|protocol          | http/https (defaults to http if not set)|
|api_token         | grafana API token|
|cert_file         | file where the TSL certificate is stored|
|username          | the simple auth user name|
|password          | the simple auth password|
|dashboardId       | a specific dashboard ID (all in case it's not specified)|
|only_actions      | a boolean flag to send only actions or probes as well (defaults to false)|
|tags              | a list of custom tags to tag annotations|
annotation_api_endpoint| defaults to '/api/annotations'|

The 'dashboardId' parameter points to the dashboard annotations are added to,
otherwise annotations will be displayed on all dashboards.

The 'only_actions' parameter allows to trace only actions, not probes. 
The 'tags' parameter allows to add custom tags to each annotation.

Refer to the official Grafana documentation for details on how to set up data
stores for InfluxDB databases. For the Grafana driver just use the default
grafana data store when configuring the annotations for your dashboard.

Then, at the proper level, configure the control driver:

```
            "controls": [
                {
                    "name": "tracing",
                    "provider": {
                        "type": "python",
                        "module": "chaosdb.grafana"
                    }
                }
            ],
```
