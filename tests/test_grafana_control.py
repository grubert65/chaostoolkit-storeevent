import responses
from chaosdb.grafana import running,                    \
                            configure_control,          \
                            before_activity_control,    \
                            after_activity_control,     \
                            post_event


@responses.activate
def test_before_activity_control():
    responses.add(responses.POST,
                  'http://localhost:80/api/annotations',
                  json={
                    "message":"Annotation added",
                    "id": 1,
                  },
                  status=200)
    responses.add(responses.POST,
                  'https://localhost:443/api/annotations',
                  json={
                    "message":"Annotation added",
                    "id": 1,
                  },
                  status=200)

    assert configure_control({
        "grafana": [{
            "dashboardId": 0,
            "host": "localhost",
            "port": 80,
            "protocol": "http",
            "tags": [
              "P2"
            ]
          },{
             "api_token": "token",
             "dashboardId": 0,
             "host": "localhost",
             "port": 443,
             "protocol": "https",
             "tags": [
              "P2"
            ]
          }]
        }, {}) == 1

    context = {
        "type": "action",
        "name": "test action",
        "provider": {
            "type": "python",
            "module": "chaosdb.grafana",
            "func": "bar",
            "arguments": {"foo": "bar"}
        }
    }
    assert before_activity_control(context, {}) == 1

@responses.activate
def test_after_activity_control():
    responses.add(responses.POST,
                  'http://localhost:80/api/annotations',
                  json={
                    "message":"Annotation added",
                    "id": 1,
                  },
                  status=200)
    responses.add(responses.POST,
                  'https://localhost:443/api/annotations',
                  json={
                    "message":"Annotation added",
                    "id": 1,
                  },
                  status=200)

    assert configure_control({
        "grafana": [{
            "dashboardId": 0,
            "host": "localhost",
            "port": 80,
            "protocol": "http",
            "tags": [
              "P2"
            ]
          },{
             "api_token": "token",
             "dashboardId": 0,
             "host": "localhost",
             "port": 443,
             "protocol": "https",
             "tags": [
              "P2"
            ]
          }]
    }, {}) == 1

    context = {
        "type": "action",
        "name": "test action",
        "provider": {
            "type": "python",
            "module": "foo",
            "func": "bar"
        }
    }
    assert after_activity_control(context, {}) == 1
