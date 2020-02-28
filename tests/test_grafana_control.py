import unittest
from chaosdb.grafana import running,                    \
                            configure_control,          \
                            before_activity_control,    \
                            after_activity_control


@unittest.skipIf(
    running() is False,
    "Test skipped: Grafana server not running")
class TestControl(unittest.TestCase):

    def test_before_activity_control(self):

        self.assertEqual(configure_control({}, {}), 1)

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
        self.assertEqual(before_activity_control(context, {}), 200)

    def test_after_activity_control(self):

        self.assertEqual(configure_control({}, {}), 1)

        context = {
            "type": "action",
            "name": "test action",
            "provider": {
                "type": "python",
                "module": "foo",
                "func": "bar"
            }
        }
        self.assertEqual(after_activity_control(context, {}), 200)


if __name__ == "__main__":
    unittest.main()
