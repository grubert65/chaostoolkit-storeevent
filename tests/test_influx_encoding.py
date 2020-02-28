import unittest
from chaosdb.influx import encode_payload_in_line_protocol


class TestInfluxPayloadEncoding(unittest.TestCase):

    def test_one_field_payload(self):

        self.assertEqual(encode_payload_in_line_protocol(
            "measurement", fields={"field1": "value1"}),
            'measurement field1="value1"')

    def test_two_fields_payload(self):

        self.assertEqual(encode_payload_in_line_protocol(
            "measurement", fields={"field1": "value1", "field2": 123}),
            'measurement field1="value1",field2=123')

    def test_fields_and_tags_payload(self):

        self.assertEqual(encode_payload_in_line_protocol(
            "measurement",
            fields={"field1": "value1", "field2": 123},
            tags={"tag1": "v1", "tag2": "v2"}
        ), 'measurement,tag1=v1,tag2=v2 field1="value1",field2=123')


if __name__ == "__main__":
    unittest.main()
