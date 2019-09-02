import unittest
import os
from chaosdb.litedb import running, \
                           configure_control, \
                           before_activity_control, \
                           after_activity_control


@unittest.skipIf(
    running() is None,
    "Test skipped: Sqlite not found")
class TestControl(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #         import pdb; pdb.set_trace()
        # trace db creation
        os.system('./scripts/trace.sh')

    def test_before_activity_control(self):

        self.assertEqual(configure_control({
            "litedb_filename": "./trace.db"
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
        self.assertEqual(before_activity_control(context, {}), True)

    def test_after_activity_control(self):

        self.assertEqual(configure_control({
            "litedb_filename": "./trace.db"
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
