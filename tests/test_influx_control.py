import unittest
from chaosdb.influx import running,                 \
                           configure_control,       \
                           before_activity_control, \
                           after_activity_control


@unittest.skipIf(
    running() is False,
    "Test skipped: InfluxDB server not running")
class TestControl(unittest.TestCase):

    #     @classmethod
    #     def setUpClass(cls):
    #         os.system('./scripts/influxd.sh')
    #   some initialization...

    def test_before_activity_control(self):

        self.assertEqual(configure_control({
            "influx": {
                "host": "localhost",
                "port": 8086,
                "http_endpoint": "/write",
                "database": "chaostoolkit"
            }
        }, {}), 1)

        context = {
            "type": "action",
            "name": "test action",
            "provider": {
                "type": "python",
                "module": "foo",
                "func": "bar",
                "arguments": {"foo": "bar"}
            }
        }
        self.assertEqual(before_activity_control(context, {}), True)

    def test_after_activity_control(self):

        self.assertEqual(configure_control({
            "influx": {
                "host": "localhost",
                "port": 8086,
                "http_endpoint": "/write",
                "database": "chaostoolkit"
            }
        }, {}), 1)

        context = {
            "type": "action",
            "name": "test action",
            "provider": {
                "type": "python",
                "module": "foo",
                "func": "bar"
            }
        }
        self.assertEqual(after_activity_control(context, {}), True)


if __name__ == "__main__":
    unittest.main()
